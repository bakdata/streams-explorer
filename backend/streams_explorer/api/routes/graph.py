from typing import Optional

from fastapi import APIRouter, Depends, WebSocket
from fastapi.exceptions import HTTPException
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from streams_explorer.api.dependencies.streams_explorer import get_streams_explorer
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.models.graph import Graph, StateUpdate
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
    logger.info("Waiting for WebSocket client...")
    await websocket.accept()
    logger.info("WebSocket client connected")
    await websocket.send_text("Connected")
    try:
        while True:
            logger.info("waiting for state update...")
            app: K8sApp = await streams_explorer.updates.get()
            logger.info("got state update")
            await websocket.send_json(
                StateUpdate(
                    id=app.id,
                    replicas_ready=app.replicas_ready,
                    replicas_total=app.replicas_total,
                ).json()
            )
    except WebSocketDisconnect:
        await websocket.close()
