from enum import Enum
from typing import Dict, List

from loguru import logger
from prometheus_api_client import PrometheusApiClientException, PrometheusConnect

from streams_explorer.core.config import settings
from streams_explorer.models.graph import Metric, Node


class PrometheusMetric(Enum):
    def __init__(self, metric, query):
        self.metric = metric
        self.query = query

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
        'sum(kafka_consumergroup_group_topic_sum_lag{group=~".+"}) by (group)',
    )
    TOPIC_SIZE = (
        "topic_size",
        "sum by(topic) (kafka_topic_partition_current_offset - kafka_topic_partition_oldest_offset)",
    )


class MetricProvider:
    def __init__(self, nodes: List[Node]):
        self._nodes: List[Node] = nodes
        self.metrics: List[Metric] = []
        self._data: Dict[str, List] = {}

    def refresh_data(self):
        pass

    def update(self):
        self.refresh_data()
        self.metrics = [
            Metric(
                node_id=node_id,
                consumer_lag=self._data["consumer_lag"].get(node.get("consumer_group")),
                messages_in=self._data["messages_in"].get(node_id),
                messages_out=self._data["messages_out"].get(node_id),
                topic_size=self._data["topic_size"].get(node_id),
            )
            for node_id, node in self._nodes
            if node_id
        ]

    def get(self) -> List[Metric]:
        self.update()
        return self.metrics


class PrometheusMetricProvider(MetricProvider):
    def __init__(self, nodes: List[Node]):
        super().__init__(nodes)
        self._prom = PrometheusConnect(url=settings.prometheus.url)

    def get_metric(self, metric: PrometheusMetric) -> List:
        try:
            return self.__prom_request(metric.query)
        except PrometheusApiClientException as e:
            logger.error(f"Error pulling {metric}: {e}")
        return []

    def __prom_request(self, query: str) -> List:
        return self._prom.custom_query(query)

    def refresh_data(self):
        logger.debug("Pulling metrics from Prometheus")
        self._data["messages_in"] = self.__get_messages_in()
        self._data["messages_out"] = self.__get_messages_out()
        self._data["consumer_lag"] = self.__get_consumer_lag()
        self._data["topic_size"] = self.__get_topic_size()

    def __get_messages_in(self) -> Dict[str, float]:
        prom_messages_in = self.get_metric(metric=PrometheusMetric.MESSAGES_IN)
        return {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2)
            for d in prom_messages_in
        }

    def __get_messages_out(self) -> Dict[str, float]:
        prom_messages_out = self.get_metric(metric=PrometheusMetric.MESSAGES_OUT)
        return {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2)
            for d in prom_messages_out
        }

    def __get_consumer_lag(self) -> Dict[str, int]:
        prom_consumer_lag = self.get_metric(metric=PrometheusMetric.CONSUMER_LAG)
        return {d["metric"]["group"]: int(d["value"][-1]) for d in prom_consumer_lag}

    def __get_topic_size(self) -> Dict[str, int]:
        prom_topic_size = self.get_metric(metric=PrometheusMetric.TOPIC_SIZE)
        return {d["metric"]["topic"]: int(d["value"][-1]) for d in prom_topic_size}
