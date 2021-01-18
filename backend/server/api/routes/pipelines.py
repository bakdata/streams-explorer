from fastapi import APIRouter, Depends

from server.api.dependencies.streams_explorer import get_streams_explorer_from_request
from server.models.pipelines import Pipelines
from server.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=Pipelines)
def pipelines(
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    return Pipelines(pipelines=streams_explorer.get_pipeline_names())
