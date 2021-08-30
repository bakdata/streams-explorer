import concurrent.futures
from typing import Dict, ValuesView

from confluent_kafka.admin import AdminClient, ConfigEntry, ConfigResource

from streams_explorer.core.config import settings


class Kafka:
    def __init__(self):
        self.__client: AdminClient = AdminClient(settings.kafka.config)
        self.__timeout: int = 1

    def __get_config(self, resource: ConfigResource) -> ValuesView:
        configs = self.__client.describe_configs(resources=[resource])
        return configs.values()

    def get_topic_config(self, topic: str) -> dict:
        topic_config = ConfigResource(ConfigResource.Type.TOPIC, topic)

        for c in concurrent.futures.as_completed(iter(self.__get_config(topic_config))):
            result: Dict[str, ConfigEntry] = c.result(timeout=self.__timeout)
            return {config.name: config.value for config in result.values()}
        return {}
