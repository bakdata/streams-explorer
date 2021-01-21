import importlib
import os
import sys
from inspect import isclass
from types import ModuleType
from typing import List, Optional, Union

from loguru import logger

from streams_explorer.core.config import settings


def load_plugin(base_class: type, all: bool = False) -> Union[type, List[type], None]:
    if not settings.plugins.path:
        return None
    path = settings.plugins.path
    sys.path.append(path)
    logger.info(f"Loading {base_class} from {path}")
    modules = []
    for file in os.listdir(path):
        if not file.endswith(".py"):
            continue

        module = importlib.import_module(file.replace(".py", ""))
        plugin_class: Optional[type] = get_class(module, base_class)
        if plugin_class is None:
            continue
        logger.info(f"Found {plugin_class} {file}")
        if not all:
            return plugin_class
        modules.append(plugin_class)
    return modules


def get_class(module: ModuleType, base_class: type) -> Optional[type]:
    for name in dir(module):
        attribute = getattr(module, name)
        if (
            attribute
            and isclass(attribute)
            and issubclass(attribute, base_class)
            and attribute != base_class
        ):
            plugin_class = attribute
            if not callable(plugin_class):
                return eval(plugin_class)
            return plugin_class
    return None
