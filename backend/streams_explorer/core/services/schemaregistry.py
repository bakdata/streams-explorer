import json

import requests
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.services.dataflow_graph import NodeNotFound

url = settings.schemaregistry.url


class SchemaRegistry:
    @staticmethod
    def get_topic_value_schema_versions(topic: str) -> list:
        logger.info(f"Fetch schema versions for topic {topic}")
        response = requests.get(f"{url}/subjects/{topic}-value/versions/")
        data = response.json()
        if response.status_code == 200:
            return data
        logger.debug(f"Error fetching schema versions for topic {topic}: {data}")
        return []

    @staticmethod
    def get_topic_value_schema(topic: str, version: int = 1) -> dict:
        try:
            logger.info(f"Fetch schema version {version} for {topic}")
            response = requests.get(f"{url}/subjects/{topic}-value/versions/{version}")
            return json.loads(response.json().get("schema"))
        except Exception:
            raise NodeNotFound()

    @staticmethod
    def get_newest_topic_value_schema(topic: str) -> dict:
        logger.info(f"Fetch newest schema for topic {topic}")
        versions = SchemaRegistry.get_topic_value_schema_versions(topic)
        if not versions:
            return {}
        newest_version = max(versions)
        return SchemaRegistry.get_topic_value_schema(topic, newest_version)
