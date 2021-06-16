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
    x: Optional[int]
    y: Optional[int]


class Metric(BaseModel):
    node_id: str
    messages_in: Optional[float]
    messages_out: Optional[float]
    consumer_lag: Optional[int]
    consumer_read_rate: Optional[float]
    topic_size: Optional[int]
    replicas: Optional[int]
    replicas_available: Optional[int]
    connector_tasks: Optional[int]


class Edge(BaseModel):
    source: str
    target: str


class Graph(BaseModel):
    directed: bool
    multigraph: bool
    graph: Any
    nodes: List[Node]
    edges: List[Edge]
