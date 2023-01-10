from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from kubernetes_asyncio.client import V1beta1CronJob, V1Job

from streams_explorer.models.k8s import K8sConfig
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source
from streams_explorer.plugins import Plugin

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sAppCronJob, K8sAppJob


@dataclass
class Extractor(Plugin):
    sources: list[Source] = field(default_factory=list)
    sinks: list[Sink] = field(default_factory=list)

    def reset(self) -> None:
        self.sources.clear()
        self.sinks.clear()


class ConnectorExtractor(Extractor):
    @abstractmethod
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        ...


class StreamsAppExtractor(Extractor):
    @abstractmethod
    def on_streaming_app_add(self, config: K8sConfig) -> None:
        ...

    @abstractmethod
    def on_streaming_app_delete(self, config: K8sConfig) -> None:
        ...


class ProducerAppExtractor(Extractor):
    @abstractmethod
    def on_job_parsing(self, job: V1Job) -> K8sAppJob | None:
        ...

    @abstractmethod
    def on_cron_job_parsing(self, cron_job: V1beta1CronJob) -> K8sAppCronJob | None:
        ...
