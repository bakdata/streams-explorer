from typing import Optional

from fastapi import APIRouter, Depends, WebSocket
from fastapi.exceptions import HTTPException
from starlette.websockets import WebSocketDisconnect

from streams_explorer.api.dependencies.streams_explorer import get_streams_explorer
from streams_explorer.models.graph import Graph
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=Graph)
async def get_positioned_graph(
    pipeline_name: Optional[str] = None,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer),
):
    if pipeline_name:
        pipeline_graph = await streams_explorer.get_positioned_pipeline_json_graph(
            pipeline_name
        )
        if pipeline_graph is None:
            raise HTTPException(
                status_code=404, detail=f"Pipeline '{pipeline_name}' not found"
            )
        return pipeline_graph
    return streams_explorer.get_positioned_json_graph()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer),
):
    """Send application state updates through WebSocket."""
    await streams_explorer.clients.connect(websocket)

    try:
        # bring client up to date by sending all current states
        for app in streams_explorer.applications.values():
            await streams_explorer.clients.send(websocket, app.to_state_update())

        # continuously update
        while True:
            # block until queue has new update
            state = await streams_explorer.updates.get()
            await streams_explorer.clients.broadcast(state)

    except WebSocketDisconnect:
        await streams_explorer.clients.disconnect(websocket)
