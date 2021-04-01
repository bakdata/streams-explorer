from typing import Type

from loguru import logger

from streams_explorer.core.services.metric_providers import (
    MetricProvider,
    PrometheusMetricProvider,
)
from streams_explorer.plugins import load_plugin


def load_metric_provider() -> Type[MetricProvider]:
    metric_provider = load_plugin(MetricProvider)
    if (
        not metric_provider
        or not isinstance(metric_provider, type)
        or not issubclass(metric_provider, MetricProvider)
    ):
        logger.info("Using default PrometheusMetricProvider")
        return PrometheusMetricProvider
    logger.info(f"Using custom MetricProvider: {metric_provider.__name__}")
    return metric_provider
