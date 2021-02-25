from typing import List, Optional, Tuple

from kubernetes.client import V1beta1CronJob
from loguru import logger

from streams_explorer.core.extractor.default.generic import GenericSink, GenericSource
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source


class ExtractorContainer:
    def __init__(self, extractors=None):
        self.extractors: List[Extractor] = extractors if extractors else []

    def add(self, extractor: Extractor):
        self.extractors.append(extractor)
        logger.info("Added extractor {}", extractor.__class__.__name__)

    def add_generic(self):
        self.add(GenericSink())
        self.add(GenericSource())

    def reset(self):
        for extractor in self.extractors:
            extractor.sinks = []
            extractor.sources = []

    def on_streaming_app_env_parsing(self, env, streaming_app_name: str):
        for extractor in self.extractors:
            extractor.on_streaming_app_env_parsing(env, streaming_app_name)

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        for extractor in self.extractors:
            connector: Optional[KafkaConnector] = extractor.on_connector_info_parsing(
                info, connector_name
            )
            if connector:
                return connector
        return None

    def on_cron_job(self, cron_job: V1beta1CronJob):
        for extractor in self.extractors:
            app = extractor.on_cron_job_parsing(cron_job)
            if app:
                return app
        return None

    def get_sources_sinks(self) -> Tuple[List[Source], List[Sink]]:
        sources: List[Source] = []
        sinks: List[Sink] = []
        for extractor in self.extractors:
            if extractor.sources:
                for source in extractor.sources:
                    sources.append(source)
            if extractor.sinks:
                for sink in extractor.sinks:
                    sinks.append(sink)
        return sources, sinks
