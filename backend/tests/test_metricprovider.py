import pytest
from prometheus_api_client import PrometheusConnect

from streams_explorer.core.services.metric_providers import (
    MetricProvider,
    PrometheusMetricProvider,
)
from streams_explorer.models.graph import Metric
from tests.test_metricprovider_data import nodes, prometheus_data


class TestPrometheusMetricProvider:
    @pytest.fixture()
    def metrics_provider(self, mocker, monkeypatch):
        metrics_provider = PrometheusMetricProvider(nodes)
        return metrics_provider

    def test_get_consumer_group(self, metrics_provider):
        node_id, node = nodes[0]  # streaming-app
        assert (
            MetricProvider.get_consumer_group(node_id, node)
            == "streams-explorer-transactionavroproducer-atm-fraud-incoming-transactions-topic"
        )
        node_id, node = nodes[4]  # connector
        assert MetricProvider.get_consumer_group(node_id, node) == "connect-demo-sink"

    def test_empty_query(self, monkeypatch, metrics_provider):
        def mock_query(*args, **kwargs):
            return []

        monkeypatch.setattr(PrometheusConnect, "custom_query", mock_query)

        result = metrics_provider.get()
        assert result == [
            Metric(
                node_id="atm-fraud-transactionavroproducer",
            ),
            Metric(
                node_id="atm-fraud-incoming-transactions-topic",
            ),
            Metric(
                node_id="atm-fraud-raw-input-topic",
            ),
            Metric(
                node_id="demo-sink",
            ),
        ]

    def test_update(self, mocker, monkeypatch, metrics_provider):
        def mock_get_metric(*args, **kwargs):
            metric = kwargs.get("metric")
            return prometheus_data[metric.metric]

        monkeypatch.setattr(PrometheusMetricProvider, "get_metric", mock_get_metric)

        result = metrics_provider.get()
        assert result == [
            Metric(
                node_id="atm-fraud-transactionavroproducer",
                consumer_lag=78,
                replicas=1,
                consumer_read_rate=64.977769,
            ),
            Metric(
                node_id="atm-fraud-incoming-transactions-topic",
                messages_in=4.8,
                messages_out=4.8,
                topic_size=0,
            ),
            Metric(
                node_id="atm-fraud-raw-input-topic",
                messages_in=0,
                messages_out=5.13,
                topic_size=75921,
            ),
            Metric(
                node_id="demo-sink",
                consumer_lag=1,
                connector_tasks=3,
            ),
        ]
