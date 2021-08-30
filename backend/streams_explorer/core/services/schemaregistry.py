import json
from typing import List

import httpx
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.services.dataflow_graph import NodeNotFound

url = settings.schemaregistry.url


def default_return(default):
    def decorator(func):
        def inner(*args, **kw):
            if url is None:
                return default
            return func(*args, **kw)

        return inner

    return decorator


class SchemaRegistry:
    @staticmethod
    @default_return([])
    def get_versions(topic: str) -> List[int]:
        logger.info(f"Fetch schema versions for topic {topic}")
        response = httpx.get(f"{url}/subjects/{topic}-value/versions/")
        if response.status_code == 200:
            data = response.json()
            return data
        logger.debug(f"Error fetching schema versions for topic {topic}: {response}")
        return []

    @staticmethod
    @default_return({})
    def get_schema(topic: str, version: int = 1) -> dict:
        try:
            logger.info(f"Fetch schema version {version} for {topic}")
            response = httpx.get(f"{url}/subjects/{topic}-value/versions/{version}")
            return json.loads(response.json().get("schema"))
        except Exception:
            raise NodeNotFound()
