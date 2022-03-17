import concurrent.futures
from typing import Any, Dict, List, Optional, Set

from cachetools.func import ttl_cache
from confluent_kafka.admin import (
    AdminClient,
    ConfigEntry,
    ConfigResource,
    PartitionMetadata,
    TopicMetadata,
)

from streams_explorer.core.config import settings


class KafkaAdminClient:
    def __init__(self):
        self._enabled: bool = settings.kafka.enable
        self._client: AdminClient
        self.__connect()

    @property
    def enabled(self):
        return self._enabled

    def __connect(self):
        if self.enabled:
            self._client = AdminClient(settings.kafka.config)

    def __describe_config(self, resource: ConfigResource) -> dict:
        return self._client.describe_configs(resources=[resource])

    def __get_resource(self, resource: ConfigResource) -> List[ConfigEntry]:
        fs = self.__describe_config(resource)
        for f in concurrent.futures.as_completed(iter(fs.values())):
            configs = f.result()
            return list(configs.values())
        return []

    def get_topic_config(self, topic: str) -> Dict[str, Any]:
        topic_resource = ConfigResource(ConfigResource.Type.TOPIC, topic)
        result = self.__get_resource(topic_resource)
        return self.format_values(result)

    def __get_topic(self, topic: str) -> Optional[TopicMetadata]:
        topics = self._client.list_topics(topic).topics
        return topics.get(topic)

    def get_topic_partitions(
        self, topic: str
    ) -> Optional[Dict[int, PartitionMetadata]]:
        metadata = self.__get_topic(topic)
        if metadata is None:
            return None
        return metadata.partitions

    @ttl_cache(maxsize=1, ttl=settings.kafka.topic_names_cache.ttl)
    def get_all_topic_names(self) -> Set[str]:
        return set(self._client.list_topics().topics.keys())

    @staticmethod
    def format_values(values: List[ConfigEntry]) -> Dict[str, Any]:
        return {
            config.name: config.value for config in values if not config.is_sensitive
        }
