import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, WebSocket
from fastapi.exceptions import HTTPException
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from streams_explorer.api.dependencies.streams_explorer import get_streams_explorer
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.models.graph import AppState, Graph, ReplicaCount
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
    try:
        while True:
            # TODO: enable
            # logger.info("waiting for state update...")
            # # block until queue has new update
            # app: K8sApp = await streams_explorer.updates.get()
            # logger.info("got state update")
            # await websocket.send_json(
            #     AppState(
            #         id=app.id, replicas=(app.replicas_ready, app.replicas_total)
            #     ).dict()
            # )

            # HACK: simulate
            app_id = "atm-fraud-transactionavroproducer"
            update = AppState(id=app_id, replicas=ReplicaCount(ready=0, total=1))
            await websocket.send_json(update.dict())
            await asyncio.sleep(1)

            update.replicas = ReplicaCount(ready=1, total=1)
            await websocket.send_json(update.dict())
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        await websocket.close()
