from loguru import logger

from streams_explorer.core.services.metric_providers import (
    MetricProvider,
    PrometheusMetricProvider,
)
from streams_explorer.plugins import load_plugin


def load_metric_provider() -> type[MetricProvider]:
    metric_provider = load_plugin(MetricProvider)
    if not metric_provider:
        logger.info("Using default PrometheusMetricProvider")
        return PrometheusMetricProvider
    logger.info(f"Using custom MetricProvider: {metric_provider.__name__}")
    return metric_provider
