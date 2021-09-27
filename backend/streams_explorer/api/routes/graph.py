from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from streams_explorer.api.dependencies.streams_explorer import (
    get_streams_explorer_from_request,
)
from streams_explorer.models.graph import Graph
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=Graph)
async def get_positioned_graph(
    pipeline_name: Optional[str] = None,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
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
