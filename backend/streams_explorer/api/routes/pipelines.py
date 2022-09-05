from fastapi import APIRouter, Depends

from streams_explorer.api.dependencies.streams_explorer import get_streams_explorer
from streams_explorer.models.pipelines import Pipelines
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=Pipelines)
def get_pipelines(
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer),
):
    return Pipelines(pipelines=streams_explorer.get_pipeline_names())
