from fastapi import APIRouter, Depends
from loguru import logger

from streams_explorer.api.dependencies.streams_explorer import get_streams_explorer
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.post("")
async def update(
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer),
):
    logger.info("(Re-)Building graphs")
    await streams_explorer.update_graph()
