from typing import Type

from loguru import logger

from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.defaultlinker import DefaultLinker
from streams_explorer.plugins import load_plugin


def load_linker() -> Type[LinkingService]:
    linker = load_plugin(LinkingService)
    if not linker or not issubclass(linker, LinkingService):
        logger.info("Using default LinkingService")
        return DefaultLinker
    logger.info(f"Using custom LinkingService: {linker.__name__}")
    return linker
