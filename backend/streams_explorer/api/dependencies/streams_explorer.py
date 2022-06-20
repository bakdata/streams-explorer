from fastapi import FastAPI
from starlette.requests import Request
from starlette.websockets import WebSocket

from streams_explorer.streams_explorer import StreamsExplorer


def get_streams_explorer_from_request(request: Request) -> StreamsExplorer:
    return get_streams_explorer(request.app)


def get_streams_explorer_from_websocket(websocket: WebSocket) -> StreamsExplorer:
    return get_streams_explorer(websocket.app)


def get_streams_explorer(app: FastAPI) -> StreamsExplorer:
    return app.state.streams_explorer
