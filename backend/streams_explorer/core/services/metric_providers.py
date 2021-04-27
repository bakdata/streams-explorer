from typing import Dict, List, Optional

from loguru import logger
from networkx.classes.reportviews import NodeDataView
from prometheus_api_client import PrometheusApiClientException, PrometheusConnect

from streams_explorer.core.config import settings
from streams_explorer.models.graph import Metric
from streams_explorer.models.node_types import NodeTypesEnum


class PrometheusMetricInterface():
    class MetricPair:
        def __init__(self, metric: str, query: str):
            self.metric = metric
            self.query = query

    def get_messages_in_metric_pair(self) -> MetricPair:
        return PrometheusMetricInterface.MetricPair("messages_in", self.get_messages_in_metric_name())

    def get_messages_in_metric_name(self) -> str:
        """Returns the name of the message in rate metric."""
        pass

    def get_messages_out_metric_pair(self) -> MetricPair:
        return PrometheusMetricInterface.MetricPair("messages_out", self.get_messages_out_metric_name())

    def get_messages_out_metric_name(self) -> str:
        """Returns the name of the message out rate metric."""
        pass

    def get_consumer_lag_metric_pair(self) -> MetricPair:
        return PrometheusMetricInterface.MetricPair("consumer_lag", self.get_consumer_lag_metric_name())

    def get_consumer_lag_metric_name(self) -> str:
        """Returns the name of the consumer lag metric."""
        pass

    def get_consumer_read_rate_metric_pair(self) -> MetricPair:
        return PrometheusMetricInterface.MetricPair("consumer_read_rate", self.get_consumer_read_rate_metric_name())

    def get_consumer_read_rate_metric_name(self) -> str:
        """Returns the name of the consumer read rate metric."""
        pass

    def get_topic_size_metric_pair(self) -> MetricPair:
        return PrometheusMetricInterface.MetricPair("topic_size", self.get_topic_size_metric_name())

    def get_topic_size_metric_name(self) -> str:
        """Returns the name of the topic size (max - min offset) metric."""
        pass

    def get_replicas_metric_pair(self) -> MetricPair:
        return PrometheusMetricInterface.MetricPair("replicas", self.get_replicas_metric_name())

    def get_replicas_metric_name(self) -> str:
        """Returns the name of the replicas (pod count) metric."""
        pass

    def get_connector_tasks_metric_pair(self) -> MetricPair:
        return PrometheusMetricInterface.MetricPair("connector_tasks", self.get_connector_tasks_metric_name())

    def get_connector_tasks_metric_name(self) -> str:
        """Returns the name of the conector task count metric."""
        pass


class DanielqsjKafkaExporterMetrics:

    def get_topic_size_metric_name(self) -> str:
        return "sum by(topic) (kafka_topic_partition_current_offset - kafka_topic_partition_oldest_offset)"

    def get_messages_in_metric_name(self) -> str:
        return "sum by(topic) (rate(kafka_topic_partition_current_offset[5m]))"


class KafkaLagExporterMetrics:

    def get_messages_out_metric_name(self) -> str:
        return "sum by(topic) (rate(kafka_consumergroup_group_offset[5m]) >= 0)"

    def get_consumer_lag_metric_name(self) -> str:
        return 'sum by(group) (kafka_consumergroup_group_topic_sum_lag{group=~".+"})'

    def get_consumer_read_rate_metric_name(self) -> str:
        return 'sum by(group) (rate(kafka_consumergroup_group_offset{group=~".+"}[5m]) >= 0)'


class BundledPrometheusMetrics(PrometheusMetricInterface, DanielqsjKafkaExporterMetrics, KafkaLagExporterMetrics):

    def get_replicas_metric_name(self) -> str:
        return "sum by(deployment) (kube_deployment_status_replicas)"

    def get_connector_tasks_metric_name(self) -> str:
        return "sum by(connector) (kafka_connect_connector_tasks_state == 1) or clamp_max(sum by(connector) (kafka_connect_connector_tasks_state), 0)"


class MetricProvider:
    def __init__(self, nodes: NodeDataView):
        self._nodes: NodeDataView = nodes
        self.metrics: List[Metric] = []
        self._data: Dict[str, dict] = {}

    def refresh_data(self):
        pass

    @staticmethod
    def get_consumer_group(node_id: str, node: dict) -> Optional[str]:
        node_type: NodeTypesEnum = node["node_type"]
        if node_type == NodeTypesEnum.CONNECTOR:
            return f"connect-{node_id}"
        return node.get(settings.k8s.consumer_group_annotation)

    def update(self):
        self.refresh_data()
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
                connector_tasks=self._data["connector_tasks"].get(node_id),
            )
            for node_id, node in self._nodes
            if node_id
        ]

    def get(self) -> List[Metric]:
        self.update()
        return self.metrics


class PrometheusMetricProvider(MetricProvider):
    def __init__(self, nodes: NodeDataView, prometheus_metrics: PrometheusMetricInterface = None):
        super().__init__(nodes)
        if prometheus_metrics is None:
            self._prometheus_metrics = BundledPrometheusMetrics()
        else:
            self._prometheus_metrics = prometheus_metrics
        self._prom = PrometheusConnect(url=settings.prometheus.url)

    def get_prometheus_metrics(self) -> PrometheusMetricInterface:
        return self._prometheus_metrics

    def get_metric(self, metric: PrometheusMetricInterface.MetricPair) -> List:
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
        self._data["consumer_read_rate"] = self.__get_consumer_read_rate()
        self._data["topic_size"] = self.__get_topic_size()
        self._data["replicas"] = self.__get_replicas()
        self._data["connector_tasks"] = self.__get_connector_tasks()

    def __get_messages_in(self) -> Dict[str, float]:
        prom_messages_in = self.get_metric(metric=self.get_prometheus_metrics().get_messages_in_metric_pair())
        return {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2)
            for d in prom_messages_in
        }

    def __get_messages_out(self) -> Dict[str, float]:
        prom_messages_out = self.get_metric(metric=self.get_prometheus_metrics().get_messages_out_metric_pair())
        return {
            d["metric"]["topic"]: round(float(d["value"][-1]), 2)
            for d in prom_messages_out
        }

    def __get_consumer_lag(self) -> Dict[str, int]:
        prom_consumer_lag = self.get_metric(metric=self.get_prometheus_metrics().get_consumer_lag_metric_pair())
        return {d["metric"]["group"]: int(d["value"][-1]) for d in prom_consumer_lag}

    def __get_consumer_read_rate(self) -> Dict[str, float]:
        prom_consumer_read_rate = self.get_metric(
            metric=self.get_prometheus_metrics().get_consumer_read_rate_metric_pair()
        )
        return {
            d["metric"]["group"]: float(d["value"][-1]) for d in prom_consumer_read_rate
        }

    def __get_topic_size(self) -> Dict[str, int]:
        prom_topic_size = self.get_metric(metric=self.get_prometheus_metrics().get_topic_size_metric_pair())
        return {d["metric"]["topic"]: int(d["value"][-1]) for d in prom_topic_size}

    def __get_replicas(self) -> Dict[str, int]:
        prom_replicas = self.get_metric(metric=self.get_prometheus_metrics().get_replicas_metric_pair())
        return {d["metric"]["deployment"]: int(d["value"][-1]) for d in prom_replicas}

    def __get_connector_tasks(self) -> Dict[str, int]:
        prom_connector_tasks = self.get_metric(metric=self.get_prometheus_metrics().get_connector_tasks_metric_pair())
        return {
            d["metric"]["connector"]: int(d["value"][-1]) for d in prom_connector_tasks
        }
