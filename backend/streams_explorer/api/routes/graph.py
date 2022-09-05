from fastapi import APIRouter, Depends, WebSocket
from fastapi.exceptions import HTTPException
from starlette.websockets import WebSocketDisconnect

from streams_explorer.api.dependencies.streams_explorer import get_streams_explorer
from streams_explorer.core.services.dataflow_graph import PipelineNotFound
from streams_explorer.models.graph import Graph
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=Graph)
async def get_positioned_graph(
    pipeline_name: str | None = None,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer),
):
    if pipeline_name:
        try:
            return await streams_explorer.get_positioned_pipeline_json_graph(
                pipeline_name
            )
        except PipelineNotFound:
            raise HTTPException(
                status_code=404, detail=f"Pipeline '{pipeline_name}' not found"
            )
    return streams_explorer.get_positioned_json_graph()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer),
):
    """Send application state updates through WebSocket."""
    await streams_explorer.client_manager.connect(websocket)

    try:
        # bring client up to date
        await streams_explorer.update_client_full(websocket)

        # keep websocket open, allows continuous update
        while websocket:
            await websocket.receive_text()

    except WebSocketDisconnect:
        return
    finally:
        await streams_explorer.client_manager.disconnect(websocket)
