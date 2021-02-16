from typing import Dict, List, Optional, Set

import requests
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.extractors import extractor_container
from streams_explorer.models.kafka_connector import KafkaConnector

url = settings.kafkaconnect.url
protected_keys: Dict[str, Set[str]] = {}


class KafkaConnect:
    @staticmethod
    def get_connectors() -> list:
        response = requests.get(f"{url}/connectors")
        return response.json()

    @staticmethod
    def get_connector_info(connector_name: str) -> dict:
        logger.info("Get connector information for {}", connector_name)
        response = requests.get(f"{url}/connectors/{connector_name}")
        info: dict = response.json()
        return info

    @staticmethod
    def get_connector_config(connector_name: str) -> dict:
        info = KafkaConnect.get_connector_info(connector_name)
        return KafkaConnect.sanitize_connector_config(info["config"])

    @staticmethod
    def extract_connector_class_basename(connector_class: str) -> str:
        if "." in connector_class:
            return connector_class.rsplit(".", 1)[-1]
        return connector_class

    @staticmethod
    def retrieve_connector_class_protected_keys(
        connector_class: str, config: dict
    ) -> None:
        response = requests.put(
            f"{url}/connector-plugins/{connector_class}/config/validate",
            json=config,
        )
        if not response.ok:
            logger.warning(
                'Couldn\'t retrieve connector class validation for "{}": {}',
                connector_class,
                response,
            )
            return
        data = response.json()
        protected_keys[connector_class] = {
            config["value"]["name"]
            for config in data["configs"]
            if config["definition"]["type"] == "PASSWORD"
        }

    @staticmethod
    def sanitize_connector_config(config: dict) -> dict:
        connector_class = KafkaConnect.extract_connector_class_basename(
            config["connector.class"]
        )
        if connector_class not in protected_keys:
            KafkaConnect.retrieve_connector_class_protected_keys(
                connector_class, config
            )
        for key in protected_keys[connector_class].intersection(config):
            config[key] = "[hidden]"
            logger.debug('Sanitized connector config "{}"', key)
        return config

    @staticmethod
    def connectors() -> List[KafkaConnector]:
        protected_keys.clear()
        connectors = KafkaConnect.get_connectors()
        out = []
        for name in connectors:
            info = KafkaConnect.get_connector_info(name)
            connector: Optional[
                KafkaConnector
            ] = extractor_container.on_connector_info_parsing(info, name)
            if connector:
                out.append(connector)
            else:
                logger.warning("Failed to parse connector {}", name)
        return out
