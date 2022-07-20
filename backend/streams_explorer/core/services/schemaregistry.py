from __future__ import annotations

import json
from typing import Callable, ParamSpec, TypeVar

import httpx
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.services.dataflow_graph import NodeNotFound

url: str | None = settings.schemaregistry.url

T = TypeVar("T")
P = ParamSpec("P")


def default_return():
    """Returns an empty instance of the functions return type if Schema Registry is disabled."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        def inner(*args: P.args, **kw: P.kwargs) -> T:
            if url is None:
                ret: type[T] = eval(func.__annotations__["return"])
                return ret()
            return func(*args, **kw)

        return inner

    return decorator


class SchemaRegistry:
    @staticmethod
    @default_return()
    def get_versions(topic: str) -> list[int]:
        logger.info(f"Fetch schema versions for topic {topic}")
        response = httpx.get(f"{url}/subjects/{topic}-value/versions/")
        if response.status_code == 200:
            data = response.json()
            return data
        logger.debug(f"Error fetching schema versions for topic {topic}: {response}")
        return []

    @staticmethod
    @default_return()
    def get_schema(topic: str, version: int = 1) -> dict:
        try:
            logger.info(f"Fetch schema version {version} for {topic}")
            response = httpx.get(f"{url}/subjects/{topic}-value/versions/{version}")
            return json.loads(response.json().get("schema"))
        except Exception:
            raise NodeNotFound()
