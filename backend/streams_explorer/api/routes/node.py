from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from starlette import status

from streams_explorer.api.dependencies.streams_explorer import (
    get_streams_explorer_from_request,
)
from streams_explorer.models.node_information import NodeInformation
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("/{node_id}", response_model=NodeInformation)
async def node_info(
    node_id: str,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    try:
        return streams_explorer.get_node_information(node_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Could not find information for node with name "{node_id}"',
        )


@router.get("/linking/{node_id}", response_model=str)
def linking(
    node_id: str,
    link_type: Optional[str] = None,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    url = streams_explorer.get_link(node_id, link_type)
    logger.info(f"Redirecting to {url}")
    return url
