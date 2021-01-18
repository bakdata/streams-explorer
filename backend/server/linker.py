from typing import Type

from server.core.services.linking_services import LinkingService
from server.defaultlinker import DefaultLinker
from server.plugins import load_plugin


def load_linker() -> Type[LinkingService]:
    linker = load_plugin(LinkingService)
    if not isinstance(linker, LinkingService):
        return DefaultLinker
    return linker
