from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from kubernetes_asyncio.client import V1beta1CronJob, V1Job
from loguru import logger

from streams_explorer.core.extractor.default.generic import GenericSink, GenericSource
from streams_explorer.core.extractor.extractor import (
    ConnectorExtractor,
    Extractor,
    ProducerAppExtractor,
    StreamsAppExtractor,
)
from streams_explorer.models.k8s import K8sConfig
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sAppCronJob, K8sAppJob


class SourcesSinks(NamedTuple):
    sources: list[Source]
    sinks: list[Sink]


class ExtractorContainer:
    def __init__(self, extractors: list[Extractor] | None = None) -> None:
        self.extractors: list[Extractor] = extractors if extractors else []

    def add(self, extractor: Extractor) -> None:
        self.extractors.append(extractor)
        logger.info("Added extractor {}", extractor.__class__.__name__)

    def add_generic(self) -> None:
        self.add(GenericSink())
        self.add(GenericSource())

    def reset(self) -> None:
        for extractor in self.extractors:
            extractor.reset()

    def reset_connectors(self) -> None:
        for extractor in self.extractors:
            if isinstance(extractor, ConnectorExtractor):
                extractor.reset()

    def on_streaming_app_add(self, config: K8sConfig) -> None:
        for extractor in self.extractors:
            if isinstance(extractor, StreamsAppExtractor):
                extractor.on_streaming_app_add(config)

    def on_streaming_app_delete(self, config: K8sConfig) -> None:
        for extractor in self.extractors:
            if isinstance(extractor, StreamsAppExtractor):
                extractor.on_streaming_app_delete(config)

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        for extractor in self.extractors:
            if isinstance(extractor, ConnectorExtractor):
                if connector := extractor.on_connector_info_parsing(
                    info, connector_name
                ):
                    return connector

    def on_job(self, job: V1Job) -> K8sAppJob | None:
        for extractor in self.extractors:
            if isinstance(extractor, ProducerAppExtractor):
                if app := extractor.on_job_parsing(job):
                    return app

    def on_cron_job(self, cron_job: V1beta1CronJob) -> K8sAppCronJob | None:
        for extractor in self.extractors:
            if isinstance(extractor, ProducerAppExtractor):
                if app := extractor.on_cron_job_parsing(cron_job):
                    return app

    def get_sources_sinks(self) -> SourcesSinks:
        sources: list[Source] = []
        sinks: list[Sink] = []
        for extractor in self.extractors:
            sources.extend(extractor.sources)
            sinks.extend(extractor.sinks)
        return SourcesSinks(sources, sinks)
