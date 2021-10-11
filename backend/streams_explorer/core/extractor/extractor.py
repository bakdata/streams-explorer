from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from kubernetes.client import V1beta1CronJob

from streams_explorer.models.k8s_config import K8sConfig
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sAppCronJob


class Extractor:
    sources: List[Source] = []
    sinks: List[Sink] = []

    def on_streaming_app_config_parsing(self, config: K8sConfig):
        ...

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        ...

    def on_cron_job_parsing(self, cron_job: V1beta1CronJob) -> Optional[K8sAppCronJob]:
        ...

    @staticmethod
    def split_topics(topics: Optional[str]) -> List[str]:
        if topics:
            return topics.replace(" ", "").split(",")
        return []
