from fastapi import APIRouter, Depends

from streams_explorer.api.dependencies.streams_explorer import get_streams_explorer
from streams_explorer.models.graph import Metric
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=list[Metric])
async def get_metrics(
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer),
):
    return await streams_explorer.get_metrics()
