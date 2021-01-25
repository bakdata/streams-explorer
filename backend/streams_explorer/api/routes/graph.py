from typing import Optional

from fastapi import APIRouter, Depends

from streams_explorer.api.dependencies.streams_explorer import (
    get_streams_explorer_from_request,
)
from streams_explorer.models.graph import Graph
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=Graph)
async def graph_positioned(
    pipeline_name: Optional[str] = None,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    if pipeline_name:
        return streams_explorer.get_positioned_pipeline_json_graph(pipeline_name)
    return streams_explorer.get_positioned_json_graph()
