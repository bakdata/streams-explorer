from enum import Enum

from pydantic import BaseModel

from streams_explorer.core.services.dataflow_graph import NodeTypesEnum


class NodeInfoType(str, Enum):
    JSON = "json"
    BASIC = "basic"
    LINK = "link"


class NodeInfoListItem(BaseModel):
    name: str
    value: str | dict
    type: NodeInfoType


class NodeInformation(BaseModel):
    node_id: str
    node_type: NodeTypesEnum
    info: list[NodeInfoListItem]
