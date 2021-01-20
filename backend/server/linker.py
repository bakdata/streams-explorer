from typing import Type

from loguru import logger

from server.core.services.linking_services import LinkingService
from server.defaultlinker import DefaultLinker
from server.plugins import load_plugin


def load_linker() -> Type[LinkingService]:
    linker = load_plugin(LinkingService)
    if not linker or not issubclass(linker, LinkingService):
        logger.info("Using default LinkingService")
        return DefaultLinker
    logger.info(f"Using custom LinkingService: {linker.__name__}")
    return linker
