from enum import Enum
from typing import Callable, Dict, List, Optional

import httpx
from loguru import logger
from networkx.classes.reportviews import NodeDataView

from streams_explorer.core.config import settings
from streams_explorer.models.graph import Metric
from streams_explorer.models.node_types import NodeTypesEnum


class PrometheusMetric(Enum):
    def __init__(self, metric: str, query: str, transformer: Callable):
        self.metric: str = metric
        self.query: str = query
        self.transformer: Callable = transformer

    MESSAGES_IN = (
        "messages_in",
        "sum by(topic) (rate(kafka_topic_partition_current_offset[5m]))",
        lambda result: {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2) for d in result
        },
    )
    MESSAGES_OUT = (
        "messages_out",
        "sum by(topic) (rate(kafka_consumergroup_group_offset[5m]) >= 0)",
        lambda result: {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2) for d in result
        },
    )
    CONSUMER_LAG = (
        "consumer_lag",
        'sum by(group) (kafka_consumergroup_group_topic_sum_lag{group=~".+"})',
        lambda result: {d["metric"]["group"]: int(d["value"][-1]) for d in result},
    )
    CONSUMER_READ_RATE = (
        "consumer_read_rate",
        'sum by(group) (rate(kafka_consumergroup_group_offset{group=~".+"}[5m]) >= 0)',
        lambda result: {d["metric"]["group"]: float(d["value"][-1]) for d in result},
    )
    TOPIC_SIZE = (
        "topic_size",
        "sum by(topic) (kafka_topic_partition_current_offset - kafka_topic_partition_oldest_offset)",
        lambda result: {d["metric"]["topic"]: int(d["value"][-1]) for d in result},
    )
    REPLICAS = (
        "replicas",
        "sum by(deployment) (kube_deployment_status_replicas)",
        lambda result: {d["metric"]["deployment"]: int(d["value"][-1]) for d in result},
    )
    REPLICAS_AVAILABLE = (
        "replicas_available",
        "sum by(deployment) (kube_deployment_status_replicas_available)",
        lambda result: {d["metric"]["deployment"]: int(d["value"][-1]) for d in result},
    )
    CONNECTOR_TASKS = (
        "connector_tasks",
        "sum by(connector) (kafka_connect_connector_tasks_state == 1) or clamp_max(sum by(connector) (kafka_connect_connector_tasks_state), 0)",
        lambda result: {d["metric"]["connector"]: int(d["value"][-1]) for d in result},
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
        self._client = httpx.AsyncClient()

    async def _pull_metric(self, metric: PrometheusMetric) -> list:
        try:
            return await self._query(metric.query)
        except PrometheusException as e:
            logger.error(f"Error pulling {metric}: {e}")
        return []

    async def _query(self, query: str) -> list:
        r = await self._client.get(
            f"{settings.prometheus.url}/api/v1/query", params={"query": query}
        )
        data = r.json()
        if data and "data" in data and "result" in data["data"]:
            return data["data"]["result"]
        raise PrometheusException

    async def refresh_data(self):
        logger.debug("Pulling metrics from Prometheus")
        for metric in PrometheusMetric:
            self._data[metric.metric] = await self._process_metric(metric)

    async def _process_metric(self, metric: PrometheusMetric) -> dict:
        result = await self._pull_metric(metric)
        return metric.transformer(result)
