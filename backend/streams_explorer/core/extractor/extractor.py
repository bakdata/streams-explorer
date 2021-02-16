from typing import List, Optional

from kubernetes.client import V1beta1CronJob

from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source


class Extractor:
    sources: List[Source] = []
    sinks: List[Sink] = []

    def on_streaming_app_env_parsing(self, env, streaming_app_name: str):
        pass

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        pass

    def on_cron_job_parsing(self, cron_job: V1beta1CronJob):
        pass

    @staticmethod
    def split_topics(topics: Optional[str]) -> List[str]:
        if topics:
            return topics.replace(" ", "").split(",")
        return []
