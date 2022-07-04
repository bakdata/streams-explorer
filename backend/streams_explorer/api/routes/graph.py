from typing import Optional

from fastapi import APIRouter, Depends, WebSocket
from fastapi.exceptions import HTTPException
from loguru import logger
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
    logger.info("Waiting for WebSocket client...")
    await websocket.accept()
    logger.info("WebSocket client connected")
    await websocket.send_text("Connected")  # TODO: remove

    # send all states
    for state in streams_explorer.applications.values():
        await websocket.send_json(state.to_state_update().dict())

    # continuous update
    try:
        while True:
            # block until queue has new update
            state = await streams_explorer.updates.get()
            await websocket.send_json(state.dict())

    except WebSocketDisconnect:
        await websocket.close()
