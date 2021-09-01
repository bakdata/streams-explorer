import concurrent.futures
from typing import Dict, List

from confluent_kafka.admin import AdminClient, ConfigEntry, ConfigResource

from streams_explorer.core.config import settings


class Kafka:
    def __init__(self):
        self._client: AdminClient = AdminClient(settings.kafka.config)

    def __describe_config_values(self, resource: ConfigResource) -> list:
        configs = self._client.describe_configs(resources=[resource])
        return list(configs.values())

    def __get_resource(self, resource: ConfigResource) -> List[ConfigEntry]:
        for c in concurrent.futures.as_completed(
            iter(self.__describe_config_values(resource))
        ):
            return c.result()
        return []

    def get_topic_config(self, topic: str) -> Dict[str, str]:
        topic_resource = ConfigResource(ConfigResource.Type.TOPIC, topic)
        result = self.__get_resource(topic_resource)
        return self.format_values(result)

    @staticmethod
    def format_values(values: List[ConfigEntry]) -> Dict[str, str]:
        return {
            config.name: config.value for config in values if not config.is_sensitive
        }
