import concurrent.futures
from typing import Dict, ValuesView

from confluent_kafka.admin import AdminClient, ConfigEntry, ConfigResource

from streams_explorer.core.config import settings


class Kafka:
    def __init__(self):
        self.__client: AdminClient = AdminClient(settings.kafka.config)
        self.__timeout: int = 1

    def __describe_config_values(self, resource: ConfigResource) -> ValuesView:
        configs = self.__client.describe_configs(resources=[resource])
        return configs.values()

    def __get_resource(self, resource: ConfigResource) -> Dict[str, ConfigEntry]:
        for c in concurrent.futures.as_completed(
            iter(self.__describe_config_values(resource))
        ):
            result: Dict[str, ConfigEntry] = c.result(timeout=self.__timeout)
            return result
        return {}

    @staticmethod
    def __format_values(values: ValuesView[ConfigEntry]) -> Dict[str, str]:
        return {config.name: config.value for config in values}

    def get_topic_config(self, topic: str) -> Dict[str, str]:
        topic_resource = ConfigResource(ConfigResource.Type.TOPIC, topic)
        result = self.__get_resource(topic_resource)
        return self.__format_values(result.values())
