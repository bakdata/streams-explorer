from typing import Callable

from fastapi import FastAPI

from server.extractors import load_extractors
from server.linker import load_linker
from server.streams_explorer import StreamsExplorer


def setup_default(app: FastAPI) -> Callable:
    async def setup() -> None:
        load_extractors()
        linking_service = load_linker()
        app.state.streams_explorer = StreamsExplorer(linking_service=linking_service())
        app.state.streams_explorer.setup()
        app.state.streams_explorer.update()

    return setup
