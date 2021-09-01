import concurrent.futures
from typing import Any, Dict, List

from confluent_kafka.admin import AdminClient, ConfigEntry, ConfigResource

from streams_explorer.core.config import settings


class Kafka:
    def __init__(self):
        self._client: AdminClient = AdminClient(settings.kafka.config)

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

    @staticmethod
    def format_values(values: List[ConfigEntry]) -> Dict[str, Any]:
        return {
            config.name: config.value for config in values if not config.is_sensitive
        }
