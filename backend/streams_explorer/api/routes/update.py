from fastapi import APIRouter, Depends
from loguru import logger

from streams_explorer.api.dependencies.streams_explorer import (
    get_streams_explorer_from_request,
)
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.post("")
async def update(
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    logger.info("(Re-)Building graphs")
    streams_explorer.update()
