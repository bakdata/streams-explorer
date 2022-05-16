from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from kubernetes_asyncio.client import V1beta1CronJob
from loguru import logger

from streams_explorer.core.extractor.default.generic import GenericSink, GenericSource
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.k8s_config import K8sConfig
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sAppCronJob


class SourcesSinks(NamedTuple):
    sources: list[Source]
    sinks: list[Sink]


class ExtractorContainer:
    def __init__(self, extractors: list[Extractor] | None = None):
        self.extractors: list[Extractor] = extractors if extractors else []

    def add(self, extractor: Extractor):
        self.extractors.append(extractor)
        logger.info("Added extractor {}", extractor.__class__.__name__)

    def add_generic(self):
        self.add(GenericSink())
        self.add(GenericSource())

    def reset(self):
        for extractor in self.extractors:
            extractor.reset()

    def reset_connector(self):
        for extractor in self.extractors:
            extractor.reset_connector()

    def on_streaming_app_add(self, config: K8sConfig):
        for extractor in self.extractors:
            extractor.on_streaming_app_add(config)

    def on_streaming_app_delete(self, config: K8sConfig):
        for extractor in self.extractors:
            extractor.on_streaming_app_delete(config)

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        for extractor in self.extractors:
            if connector := extractor.on_connector_info_parsing(info, connector_name):
                return connector
        return None

    def on_cron_job(self, cron_job: V1beta1CronJob) -> K8sAppCronJob | None:
        for extractor in self.extractors:
            if app := extractor.on_cron_job_parsing(cron_job):
                return app
        return None

    def get_sources_sinks(self) -> SourcesSinks:
        sources: list[Source] = []
        sinks: list[Sink] = []
        for extractor in self.extractors:
            sources.extend(extractor.sources)
            sinks.extend(extractor.sinks)
        return SourcesSinks(sources, sinks)
