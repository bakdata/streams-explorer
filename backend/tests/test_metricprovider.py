import textwrap
from pathlib import Path

import pytest
from prometheus_api_client import PrometheusConnect

from streams_explorer.core.config import settings
from streams_explorer.core.services.metric_providers import (
    MetricProvider,
    PrometheusMetricProvider,
)
from streams_explorer.metric_provider import load_metric_provider
from streams_explorer.models.graph import Metric
from tests.test_metricprovider_data import nodes, prometheus_data


class TestMetricProvider:
    fake_metric_provider = textwrap.dedent(
        """\
        from typing import List, Tuple

        from streams_explorer.core.services.metric_providers import MetricProvider
        from streams_explorer.models.graph import Metric


        class FakeMetricProvider(MetricProvider):
            def __init__(self, nodes: List[Tuple[str, dict]]):
                super().__init__(nodes)
    """
    )

    def test_load_default_metric_provider(self):
        metric_provider = load_metric_provider()(nodes)
        assert type(metric_provider) is PrometheusMetricProvider

    def test_load_metric_provider_plugin(self):
        settings.plugins.path = Path.cwd() / "plugins"
        fake_metric_provider_path = settings.plugins.path / "fake_metric_provider.py"
        try:
            with open(fake_metric_provider_path, "w") as f:
                f.write(self.fake_metric_provider)

            metric_provider = load_metric_provider()(nodes)

            assert isinstance(metric_provider, MetricProvider)
            assert not isinstance(metric_provider, PrometheusMetricProvider)
            assert metric_provider.__class__.__name__ == "FakeMetricProvider"
        finally:
            fake_metric_provider_path.unlink()


class TestPrometheusMetricProvider:
    @pytest.fixture()
    def metric_provider(self):
        metric_provider = PrometheusMetricProvider(nodes)
        return metric_provider

    def test_get_consumer_group(self):
        node_id, node = nodes[0]  # streaming-app
        assert (
            MetricProvider.get_consumer_group(node_id, node)
            == "streams-explorer-transactionavroproducer-atm-fraud-incoming-transactions-topic"
        )
        node_id, node = nodes[4]  # connector
        assert MetricProvider.get_consumer_group(node_id, node) == "connect-demo-sink"

    def test_empty_query(self, monkeypatch, metric_provider):
        def mock_query(*args, **kwargs):
            return []

        monkeypatch.setattr(PrometheusConnect, "custom_query", mock_query)

        result = metric_provider.get()
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

    def test_update(self, monkeypatch, metric_provider):
        def mock_get_metric(*args, **kwargs):
            metric = kwargs.get("metric")
            return prometheus_data[metric.metric]

        monkeypatch.setattr(PrometheusMetricProvider, "get_metric", mock_get_metric)

        result = metric_provider.get()
        assert result == [
            Metric(
                node_id="atm-fraud-transactionavroproducer",
                consumer_lag=78,
                replicas=1,
                replicas_available=0,
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
