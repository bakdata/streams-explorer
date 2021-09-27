from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from starlette import status

from streams_explorer.api.dependencies.streams_explorer import (
    get_streams_explorer_from_request,
)
from streams_explorer.core.services.schemaregistry import SchemaRegistry
from streams_explorer.models.node_information import NodeInformation
from streams_explorer.streams_explorer import StreamsExplorer

router = APIRouter()


@router.get("/{node_id}", response_model=NodeInformation)
async def get_node_info(
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


@router.get("/{node_id}/schema", response_model=List[int])
async def get_node_schema_versions(node_id: str):
    return SchemaRegistry.get_versions(node_id)


@router.get("/{node_id}/schema/{version}", response_model=dict)
async def get_node_schema(node_id: str, version: int):
    return SchemaRegistry.get_schema(node_id, version=version)


@router.get("/linking/{node_id}", response_model=str)
def get_linking(
    node_id: str,
    link_type: Optional[str] = None,
    streams_explorer: StreamsExplorer = Depends(get_streams_explorer_from_request),
):
    url = streams_explorer.get_link(node_id, link_type)
    logger.info(f"Redirecting to {url}")
    return url
