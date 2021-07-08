from enum import Enum
from typing import Dict, List, Optional

import aiohttp
from loguru import logger
from networkx.classes.reportviews import NodeDataView

from streams_explorer.core.config import settings
from streams_explorer.models.graph import Metric
from streams_explorer.models.node_types import NodeTypesEnum


class PrometheusMetric(Enum):
    def __init__(self, metric: str, query: str):
        self.metric: str = metric
        self.query: str = query

    MESSAGES_IN = (
        "messages_in",
        "sum by(topic) (rate(kafka_topic_partition_current_offset[5m]))",
    )
    MESSAGES_OUT = (
        "messages_out",
        "sum by(topic) (rate(kafka_consumergroup_group_offset[5m]) >= 0)",
    )
    CONSUMER_LAG = (
        "consumer_lag",
        'sum by(group) (kafka_consumergroup_group_topic_sum_lag{group=~".+"})',
    )
    CONSUMER_READ_RATE = (
        "consumer_read_rate",
        'sum by(group) (rate(kafka_consumergroup_group_offset{group=~".+"}[5m]) >= 0)',
    )
    TOPIC_SIZE = (
        "topic_size",
        "sum by(topic) (kafka_topic_partition_current_offset - kafka_topic_partition_oldest_offset)",
    )
    REPLICAS = (
        "replicas",
        "sum by(deployment) (kube_deployment_status_replicas)",
    )
    REPLICAS_AVAILABLE = (
        "replicas_available",
        "sum by(deployment) (kube_deployment_status_replicas_available)",
    )
    CONNECTOR_TASKS = (
        "connector_tasks",
        "sum by(connector) (kafka_connect_connector_tasks_state == 1) or clamp_max(sum by(connector) (kafka_connect_connector_tasks_state), 0)",
    )


class MetricProvider:
    def __init__(self, nodes: NodeDataView):
        self._nodes: NodeDataView = nodes
        self.metrics: List[Metric] = []
        self._data: Dict[str, dict] = {}

    async def refresh_data(self):
        pass

    @staticmethod
    def get_consumer_group(node_id: str, node: dict) -> Optional[str]:
        node_type: NodeTypesEnum = node["node_type"]
        if node_type == NodeTypesEnum.CONNECTOR:
            return f"connect-{node_id}"
        return node.get(settings.k8s.consumer_group_annotation)

    async def update(self):
        await self.refresh_data()
        self.metrics = [
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
            for node_id, node in iter(self._nodes)
            if node_id
        ]

    async def get(self) -> List[Metric]:
        await self.update()
        return self.metrics


class PrometheusException(Exception):
    pass


class PrometheusMetricProvider(MetricProvider):
    def __init__(self, nodes: NodeDataView):
        super().__init__(nodes)

    async def get_metric(
        self, session: aiohttp.ClientSession, metric: PrometheusMetric
    ) -> list:
        try:
            return await self.__query(session, metric.query)
        except PrometheusException as e:
            logger.error(f"Error pulling {metric}: {e}")
        return []

    async def __query(self, session: aiohttp.ClientSession, query: str) -> list:
        async with session.get(
            f"{settings.prometheus.url}/api/v1/query", params={"query": query}
        ) as resp:
            data = await resp.json()
            if data and "data" in data and "result" in data["data"]:
                return data["data"]["result"]
            raise PrometheusException

    async def refresh_data(self):
        logger.debug("Pulling metrics from Prometheus")
        async with aiohttp.ClientSession() as session:
            self._data["messages_in"] = await self.__get_messages_in(session)
            self._data["messages_out"] = await self.__get_messages_out(session)
            self._data["consumer_lag"] = await self.__get_consumer_lag(session)
            self._data["consumer_read_rate"] = await self.__get_consumer_read_rate(
                session
            )
            self._data["topic_size"] = await self.__get_topic_size(session)
            self._data["replicas"] = await self.__get_replicas(session)
            self._data["replicas_available"] = await self.__get_replicas_available(
                session
            )
            self._data["connector_tasks"] = await self.__get_connector_tasks(session)

    async def __get_messages_in(self, session) -> Dict[str, float]:
        prom_messages_in = await self.get_metric(
            session, metric=PrometheusMetric.MESSAGES_IN
        )
        return {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2)
            for d in prom_messages_in
        }

    async def __get_messages_out(self, session) -> Dict[str, float]:
        prom_messages_out = await self.get_metric(
            session, metric=PrometheusMetric.MESSAGES_OUT
        )
        return {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2)
            for d in prom_messages_out
        }

    async def __get_consumer_lag(self, session) -> Dict[str, int]:
        prom_consumer_lag = await self.get_metric(
            session, metric=PrometheusMetric.CONSUMER_LAG
        )
        return {d["metric"]["group"]: int(d["value"][-1]) for d in prom_consumer_lag}

    async def __get_consumer_read_rate(self, session) -> Dict[str, float]:
        prom_consumer_read_rate = await self.get_metric(
            session, metric=PrometheusMetric.CONSUMER_READ_RATE
        )
        return {
            d["metric"]["group"]: float(d["value"][-1]) for d in prom_consumer_read_rate
        }

    async def __get_topic_size(self, session) -> Dict[str, int]:
        prom_topic_size = await self.get_metric(
            session, metric=PrometheusMetric.TOPIC_SIZE
        )
        return {d["metric"]["topic"]: int(d["value"][-1]) for d in prom_topic_size}

    async def __get_replicas(self, session) -> Dict[str, int]:
        prom_replicas = await self.get_metric(session, metric=PrometheusMetric.REPLICAS)
        return {d["metric"]["deployment"]: int(d["value"][-1]) for d in prom_replicas}

    async def __get_replicas_available(self, session) -> Dict[str, int]:
        prom_replicas_available = await self.get_metric(
            session, metric=PrometheusMetric.REPLICAS_AVAILABLE
        )
        return {
            d["metric"]["deployment"]: int(d["value"][-1])
            for d in prom_replicas_available
        }

    async def __get_connector_tasks(self, session) -> Dict[str, int]:
        prom_connector_tasks = await self.get_metric(
            session, metric=PrometheusMetric.CONNECTOR_TASKS
        )
        return {
            d["metric"]["connector"]: int(d["value"][-1]) for d in prom_connector_tasks
        }
