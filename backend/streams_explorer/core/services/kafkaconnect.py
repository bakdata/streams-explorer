from typing import List, Optional, Tuple

import requests
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.extractors import extractor_container
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)

url = settings.kafkaconnect.url


class KafkaConnect:
    @staticmethod
    def get_connectors() -> list:
        response = requests.get(f"{url}/connectors")
        return response.json()

    @staticmethod
    def get_connector_info(
        connector_name: str,
    ) -> Tuple[Optional[List[str]], dict, KafkaConnectorTypesEnum]:
        logger.info(f"Get connector configuration for connector {connector_name}")
        response = requests.get(f"{url}/connectors/{connector_name}")
        config: dict = response.json()["config"]
        topics: Optional[str] = config.get("topics")
        if topics is not None:
            type = KafkaConnectorTypesEnum.SINK
        else:
            type = KafkaConnectorTypesEnum.SOURCE
            topics = config.get("transforms.changeTopic.replacement")
        return KafkaConnect.get_topics(topics), config, type

    @staticmethod
    def connectors() -> List[KafkaConnector]:
        connectors = KafkaConnect.get_connectors()
        out = []
        for connector in connectors:
            topics, config, type = KafkaConnect.get_connector_info(connector)
            if topics is not None:
                out.append(
                    KafkaConnector(
                        type=type, name=connector, topics=topics, config=config
                    )
                )
            extractor_container.on_connector_config_parsing(config, connector)
        return out

    @staticmethod
    def get_topics(topics: Optional[str]) -> Optional[List[str]]:
        if topics is not None:
            return topics.replace(" ", "").split(",")
        return None
