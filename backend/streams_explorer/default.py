from typing import Callable

from fastapi import FastAPI

from streams_explorer.extractors import load_extractors
from streams_explorer.linker import load_linker
from streams_explorer.metric_provider import load_metric_provider
from streams_explorer.streams_explorer import StreamsExplorer


def setup_default(app: FastAPI) -> Callable:
    async def setup() -> None:
        load_extractors()
        linking_service = load_linker()
        metric_provider = load_metric_provider()
        app.state.streams_explorer = StreamsExplorer(
            linking_service=linking_service(), metric_provider=metric_provider
        )
        app.state.streams_explorer.setup()

    return setup
