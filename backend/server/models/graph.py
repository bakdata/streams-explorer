from typing import Any, List, Optional

from pydantic.main import BaseModel


class Icon(BaseModel):
    img: str
    show: bool
    width: int
    height: int


class Node(BaseModel):
    id: str
    label: str
    node_type: str
    icon: Optional[Icon]
    labelPosition: str
    x: Optional[int]
    y: Optional[int]


class Metric(BaseModel):
    node_id: str
    messages_in: Optional[float] = None
    messages_out: Optional[float] = None
    consumer_lag: Optional[int] = None
    topic_size: Optional[int] = None


class Edge(BaseModel):
    source: str
    target: str


class Graph(BaseModel):
    directed: bool
    multigraph: bool
    graph: Any
    nodes: List[Node]
    edges: List[Edge]
