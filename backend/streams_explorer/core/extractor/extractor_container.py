from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Iterator, NamedTuple, TypeVar

from kubernetes_asyncio.client import V1beta1CronJob
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
    from streams_explorer.core.k8s_app import K8sAppCronJob


class SourcesSinks(NamedTuple):
    sources: list[Source]
    sinks: list[Sink]


T = TypeVar("T", bound=Extractor)


class Storage:
    def __init__(self) -> None:
        self._storage: defaultdict[type, list[Extractor]] = defaultdict(list)

    def add(self, item: Extractor) -> None:
        self._storage[item.__class__.__base__].append(item)

    def __getitem__(self, key: type[T]) -> list[T]:
        return self._storage[key]  # type:ignore

    def __iter__(self) -> Iterator[Extractor]:
        for sublist in self._storage.values():
            yield from sublist

    def __len__(self) -> int:
        return len(self._storage)

    def clear(self) -> None:
        self._storage.clear()


class ExtractorContainer:
    def __init__(self, extractors: list[Extractor] | None = None) -> None:
        self.extractors: Storage = Storage()
        if extractors:
            for extractor in extractors:
                self.extractors.add(extractor)

    def add(self, extractor: Extractor) -> None:
        self.extractors.add(extractor)
        logger.info("Added extractor {}", extractor.__class__.__name__)

    def add_generic(self) -> None:
        self.add(GenericSink())
        self.add(GenericSource())

    def reset(self) -> None:
        for extractor in self.extractors:
            extractor.reset()

    def reset_connectors(self) -> None:
        for extractor in self.extractors[ConnectorExtractor]:
            extractor.reset()

    def on_streaming_app_add(self, config: K8sConfig) -> None:
        for extractor in self.extractors[StreamsAppExtractor]:
            extractor.on_streaming_app_add(config)

    def on_streaming_app_delete(self, config: K8sConfig) -> None:
        for extractor in self.extractors[StreamsAppExtractor]:
            extractor.on_streaming_app_delete(config)

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        for extractor in self.extractors[ConnectorExtractor]:
            if connector := extractor.on_connector_info_parsing(info, connector_name):
                return connector

    def on_cron_job(self, cron_job: V1beta1CronJob) -> K8sAppCronJob | None:
        for extractor in self.extractors[ProducerAppExtractor]:
            if app := extractor.on_cron_job_parsing(cron_job):
                return app

    def get_sources_sinks(self) -> SourcesSinks:
        sources: list[Source] = []
        sinks: list[Sink] = []
        for extractor in self.extractors:
            sources.extend(extractor.sources)
            sinks.extend(extractor.sinks)
        return SourcesSinks(sources, sinks)
