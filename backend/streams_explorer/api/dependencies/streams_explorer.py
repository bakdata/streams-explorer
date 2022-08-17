from fastapi import FastAPI
from starlette.requests import Request
from starlette.websockets import WebSocket

from streams_explorer.streams_explorer import StreamsExplorer

# FIXME: Pydantic bug
# @overload
# def get_application(*, request: Request, websocket=None) -> FastAPI:
#     ...


# @overload
# def get_application(*, request=None, websocket: WebSocket) -> FastAPI:
#     ...


def get_application(
    *, request: Request | None = None, websocket: WebSocket | None = None
) -> FastAPI:
    if request:
        return request.app
    if websocket:
        return websocket.app
    raise ValueError("no request or websocket argument given")


# Pydantic doesn't support correct type annotations (Request | None & WebSocket | None)
def get_streams_explorer(*, request: Request = None, websocket: WebSocket = None) -> StreamsExplorer:  # type: ignore
    app = get_application(request=request, websocket=websocket)
    return get_streams_explorer_from_state(app)


def get_streams_explorer_from_state(app: FastAPI) -> StreamsExplorer:
    return app.state.streams_explorer
