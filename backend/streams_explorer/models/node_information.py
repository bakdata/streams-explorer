from typing import List, Union

from pydantic.main import BaseModel, Enum

from streams_explorer.core.services.dataflow_graph import NodeTypesEnum


class NodeInfoType(str, Enum):
    JSON = "json"
    BASIC = "basic"
    LINK = "link"


class NodeInfoListItem(BaseModel):
    name: str
    value: Union[str, dict]
    type: NodeInfoType


class NodeInformation(BaseModel):
    node_id: str
    node_type: NodeTypesEnum
    # Todo define types
    info: List[NodeInfoListItem]
