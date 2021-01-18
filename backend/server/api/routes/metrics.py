from typing import List

from fastapi import APIRouter, Depends

from server.api.dependencies.streams_explorer import get_streams_explorer_from_request
from server.models.graph import Metric
from server.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", response_model=List[Metric])
async def metrics(
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    return streams_explorer.get_metrics()
