from fastapi import APIRouter, Depends

from streams_explorer.api.dependencies.streams_explorer import (
    get_streams_explorer_from_request,
)
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("", status_code=200)
async def ready(
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    return {"ready": streams_explorer.ready}
