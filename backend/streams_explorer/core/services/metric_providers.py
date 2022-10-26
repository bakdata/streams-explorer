import asyncio
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable

import httpx
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.models.graph import GraphNode, Metric
from streams_explorer.models.node_types import NodeTypesEnum
from streams_explorer.plugins import Plugin


class PrometheusMetric(Enum):
    def __init__(
        self,
        metric: str,
        query: str,
        key: str,
        value_transformer: Callable[[str], float],
    ) -> None:
        self.metric: str = metric
        self.query: str = query
        self._k: str = key
        self._v: Callable[[str], float] = value_transformer

    MESSAGES_IN = (
        "messages_in",
        "sum by(topic) (rate(kafka_topic_partition_current_offset[5m]))",
        "topic",
        lambda d: round(float(d), 2),
    )
    MESSAGES_OUT = (
        "messages_out",
        "sum by(topic) (rate(kafka_consumergroup_group_offset[5m]) >= 0)",
        "topic",
        lambda d: round(float(d), 2),
    )
    CONSUMER_LAG = (
        "consumer_lag",
        'sum by(group) (kafka_consumergroup_group_topic_sum_lag{group=~".+"})',
        "group",
        int,
    )
    CONSUMER_READ_RATE = (
        "consumer_read_rate",
        'sum by(group) (rate(kafka_consumergroup_group_offset{group=~".+"}[5m]) >= 0)',
        "group",
        float,
    )
    TOPIC_SIZE = (
        "topic_size",
        "sum by(topic) (kafka_topic_partition_current_offset - kafka_topic_partition_oldest_offset)",
        "topic",
        float,
    )
    REPLICAS = (
        "replicas",
        "sum by(deployment) (kube_deployment_status_replicas)",
        "deployment",
        int,
    )
    REPLICAS_AVAILABLE = (
        "replicas_available",
        "sum by(deployment) (kube_deployment_status_replicas_available)",
        "deployment",
        int,
    )
    CONNECTOR_TASKS = (
        "connector_tasks",
        "sum by(connector) (kafka_connect_connector_tasks_state == 1) or clamp_max(sum by(connector) (kafka_connect_connector_tasks_state), 0)",
        "connector",
        int,
    )

    def transform(self, data: list) -> dict:
        return {d["metric"][self._k]: self._v(d["value"][-1]) for d in data}


def sort_topics_first(nodes: list[GraphNode]) -> list[GraphNode]:
    return sorted(nodes, key=is_topic, reverse=True)


def is_topic(node: GraphNode) -> bool:
    node_type: NodeTypesEnum = node[1]["node_type"]
    return node_type in (NodeTypesEnum.TOPIC, NodeTypesEnum.ERROR_TOPIC)


class MetricProvider(Plugin):
    def __init__(self, nodes: list[GraphNode]) -> None:
        self._nodes: list[GraphNode] = sort_topics_first(nodes)
        self._metrics: list[Metric] = []
        self._data: dict[str, dict] = {}
        self._last_refresh: datetime = datetime.min
        self._cache_ttl: timedelta = timedelta(0)

    async def refresh_data(self) -> None:
        pass

    @staticmethod
    def get_consumer_group(node_id: str, node: dict) -> str | None:
        node_type: NodeTypesEnum = node["node_type"]
        if node_type == NodeTypesEnum.CONNECTOR:
            return f"connect-{node_id}"
        return node.get(settings.k8s.consumer_group_annotation)

    async def update(self) -> None:
        await self.refresh_data()
        self._metrics = [
            Metric(
                node_id=node_id,
                consumer_lag=self._data["consumer_lag"].get(
                    self.get_consumer_group(node_id, node)
                ),
                consumer_read_rate=self._data["consumer_read_rate"].get(
                    self.get_consumer_group(node_id, node)
                ),
                messages_in=self._data["messages_in"].get(node_id),
                messages_out=self._data["messages_out"].get(node_id),
                topic_size=self._data["topic_size"].get(node_id),
                replicas=self._data["replicas"].get(node_id),
                replicas_available=self._data["replicas_available"].get(node_id),
                connector_tasks=self._data["connector_tasks"].get(node_id),
            )
            for node_id, node in self._nodes
        ]

    async def get(self) -> list[Metric]:
        now = datetime.utcnow()
        cache_age = now - self._last_refresh
        if cache_age > self._cache_ttl:
            self._last_refresh = now
            await self.update()
        else:
            logger.debug("Serving cached metrics (age {}s)", cache_age.seconds)
        return self._metrics


class PrometheusException(Exception):
    pass


class PrometheusMetricProvider(MetricProvider):
    def __init__(self, nodes: list[GraphNode]) -> None:
        super().__init__(nodes)
        self._client = httpx.AsyncClient(
            base_url=f"{settings.prometheus.url}/api/v1",
        )
        # min refresh interval (set by the frontend) is 10s, intermediate requests should be cached
        self._cache_ttl = timedelta(seconds=9)

    async def _pull_metric(self, metric: PrometheusMetric) -> list:
        try:
            return await self._query(metric.query)
        except PrometheusException:
            logger.error("Error pulling {}", metric)
            return []

    async def _query(self, query: str) -> list:
        try:
            r = await self._client.get("/query", params={"query": query})
            r.raise_for_status()
            data: dict = r.json()
            return data["data"]["result"]
        except KeyError:
            pass
        except httpx.ReadTimeout:
            logger.warning("Prometheus query '{}' timed out", query)
        except httpx.ConnectError:
            logger.error("Prometheus connection failed")
        except httpx.HTTPError as e:
            raise PrometheusException from e

        raise PrometheusException

    async def refresh_data(self) -> None:
        logger.debug("Pulling metrics from Prometheus")
        tasks = []
        for metric in PrometheusMetric:
            tasks.append(asyncio.create_task(self._process_metric(metric)))
        await asyncio.gather(*tasks)

    async def _process_metric(self, metric: PrometheusMetric) -> None:
        data = await self._pull_metric(metric)
        self._data[metric.metric] = metric.transform(data)

    async def close(self) -> None:
        await self._client.aclose()

    def __del__(self) -> None:
        """Clean up client resources on exit."""
        # from aioredis: https://github.com/aio-libs/aioredis-py/blob/ff5a8fe068ebda837d14c3b3777a6182e610854a/aioredis/client.py#L1012
        try:
            loop = asyncio.get_event_loop_policy().get_event_loop()
            if loop.is_running():
                loop.create_task(self.close())
            else:
                loop.run_until_complete(self.close())
        except Exception:
            pass
