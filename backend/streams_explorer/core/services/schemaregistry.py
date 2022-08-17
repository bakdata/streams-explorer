from __future__ import annotations

import json
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import httpx
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.services.dataflow_graph import NodeNotFound

url: str | None = settings.schemaregistry.url

T = TypeVar("T")
P = ParamSpec("P")


def default_return(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator which returns an empty instance of the function's return type, if Schema Registry is disabled."""

    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        if url is None:
            try:
                typ = eval(func.__annotations__["return"])
                return typ()
            except KeyError:
                raise Exception(f"'{func.__name__}' is missing return type annotation")
        return func(*args, **kwargs)

    return inner


class SchemaRegistry:
    @staticmethod
    @default_return
    def get_versions(topic: str) -> list[int]:
        logger.info(f"Fetch schema versions for topic {topic}")
        response = httpx.get(f"{url}/subjects/{topic}-value/versions/")
        if response.status_code == 200:
            data = response.json()
            return data
        logger.debug(f"Error fetching schema versions for topic {topic}: {response}")
        return []

    @staticmethod
    @default_return
    def get_schema(topic: str, version: int = 1) -> dict:
        try:
            logger.info(f"Fetch schema version {version} for {topic}")
            response = httpx.get(f"{url}/subjects/{topic}-value/versions/{version}")
            return json.loads(response.json().get("schema"))
        except Exception:
            raise NodeNotFound()
