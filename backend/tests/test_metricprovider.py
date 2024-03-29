import textwrap
from datetime import timedelta
from pathlib import Path

import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from streams_explorer.core.config import settings
from streams_explorer.core.services.metric_providers import (
    MetricProvider,
    PrometheusMetric,
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
        assert isinstance(metric_provider, PrometheusMetricProvider)

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
        node_id, node = nodes[3]  # connector
        assert MetricProvider.get_consumer_group(node_id, node) == "connect-demo-sink"

    @pytest.mark.asyncio
    async def test_empty_query(
        self, monkeypatch: MonkeyPatch, metric_provider: MetricProvider
    ):
        async def mock_query(*_):
            return []

        monkeypatch.setattr(PrometheusMetricProvider, "_query", mock_query)

        result = await metric_provider.get()
        assert result == [
            Metric(
                node_id="atm-fraud-incoming-transactions-topic",
            ),
            Metric(
                node_id="atm-fraud-raw-input-topic",
            ),
            Metric(
                node_id="atm-fraud-transactionavroproducer",
            ),
            Metric(
                node_id="demo-sink",
            ),
        ]

    @pytest.mark.asyncio
    async def test_update(
        self, monkeypatch: MonkeyPatch, metric_provider: MetricProvider
    ):
        async def mock_pull_metric(_, metric: PrometheusMetric):
            return prometheus_data[metric.metric]

        monkeypatch.setattr(PrometheusMetricProvider, "_pull_metric", mock_pull_metric)

        result = await metric_provider.get()
        assert result == [
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
                node_id="atm-fraud-transactionavroproducer",
                consumer_lag=78,
                replicas=1,
                replicas_available=0,
                consumer_read_rate=64.977769,
            ),
            Metric(
                node_id="demo-sink",
                consumer_lag=1,
                connector_tasks=3,
            ),
        ]

    @pytest.mark.asyncio
    async def test_caching(
        self,
        monkeypatch: MonkeyPatch,
        mocker: MockerFixture,
        metric_provider: MetricProvider,
    ):
        async def mock_pull_metric(_, metric: PrometheusMetric):
            return prometheus_data[metric.metric]

        monkeypatch.setattr(PrometheusMetricProvider, "_pull_metric", mock_pull_metric)

        update_function = mocker.spy(PrometheusMetricProvider, "update")

        for _ in range(2):
            await metric_provider.get()
        assert update_function.call_count == 1
        update_function.reset_mock()  # reset call_count

        # disable caching
        metric_provider._cache_ttl = timedelta(0)
        for _ in range(2):
            await metric_provider.get()
        assert update_function.call_count == 2
