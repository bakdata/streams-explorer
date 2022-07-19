from __future__ import annotations

import importlib
import sys
from collections.abc import Sequence
from inspect import isclass
from pathlib import Path
from types import ModuleType
from typing import Literal, TypeVar, overload

from loguru import logger

from streams_explorer.core.config import settings

T = TypeVar("T")  # Plugin type


@overload
def load_plugin(base_class: type[T], all: Literal[False] = False) -> type[T] | None:
    ...


@overload
def load_plugin(base_class: type[T], all: Literal[True]) -> Sequence[type[T]]:
    ...


def load_plugin(
    base_class: type[T], all: bool = False
) -> type[T] | Sequence[type[T]] | None:
    if not settings.plugins.path:
        return None
    path = Path(settings.plugins.path)
    sys.path.append(str(path))
    logger.info(f"Loading {base_class} from {path}")
    modules = []
    for file in path.glob("*.py"):
        module = importlib.import_module(file.stem)
        plugin_class = get_class(module, base_class)
        if plugin_class is None:
            continue
        logger.info(f"Found {plugin_class} {file}")
        if not all:
            return plugin_class
        modules.append(plugin_class)
    return modules


def get_class(module: ModuleType, base_class: type[T]) -> type[T] | None:
    for name in dir(module):
        plugin_class = getattr(module, name)
        if (
            plugin_class
            and isclass(plugin_class)
            and issubclass(plugin_class, base_class)
            and plugin_class is not base_class
        ):
            return plugin_class
