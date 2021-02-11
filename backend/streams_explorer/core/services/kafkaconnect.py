from typing import List

import requests
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.extractors import extractor_container
from streams_explorer.models.kafka_connector import KafkaConnector

url = settings.kafkaconnect.url


class KafkaConnect:
    @staticmethod
    def get_connectors() -> list:
        response = requests.get(f"{url}/connectors")
        return response.json()

    @staticmethod
    def get_connector_info(connector_name: str) -> dict:
        logger.info(f"Get connector information for {connector_name}")
        response = requests.get(f"{url}/connectors/{connector_name}")
        info: dict = response.json()
        return info

    @staticmethod
    def connectors() -> List[KafkaConnector]:
        connectors = KafkaConnect.get_connectors()
        out = []
        for name in connectors:
            info = KafkaConnect.get_connector_info(name)
            topics: List[str] = extractor_container.on_connector_config_parsing(
                info["config"], name
            )
            connector = KafkaConnector(
                name=name, config=info["config"], type=info["type"], topics=topics
            )
            out.append(connector)
        return out
