from __future__ import annotations

from typing import overload

from fastapi import FastAPI
from starlette.requests import Request
from starlette.websockets import WebSocket

from streams_explorer.streams_explorer import StreamsExplorer


def get_application(
    *, request: Request | None = None, websocket: WebSocket | None = None
) -> FastAPI:
    if request:
        return request.app
    if websocket:
        return websocket.app
    raise ValueError("no request or websocket argument given")


@overload
def get_streams_explorer(
    *, request: Request, websocket: None = None
) -> StreamsExplorer:
    ...


@overload
def get_streams_explorer(
    *, request: None = None, websocket: WebSocket
) -> StreamsExplorer:
    ...


def get_streams_explorer(*, request=None, websocket=None) -> StreamsExplorer:
    app = get_application(request=request, websocket=websocket)
    return get_streams_explorer_from_state(app)


def get_streams_explorer_from_state(app: FastAPI) -> StreamsExplorer:
    return app.state.streams_explorer
