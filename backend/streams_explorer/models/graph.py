from typing import Any, List, NamedTuple, Optional, Tuple

from pydantic import BaseModel, Field

from streams_explorer.models.k8s import K8sReason

GraphNode = Tuple[str, dict]
GraphEdge = Tuple[str, str]


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
    messages_in: Optional[float] = Field(default=None)
    messages_out: Optional[float] = Field(default=None)
    consumer_lag: Optional[int] = Field(default=None)
    consumer_read_rate: Optional[float] = Field(default=None)
    topic_size: Optional[int] = Field(default=None)
    replicas: Optional[int] = Field(default=None)
    replicas_available: Optional[int] = Field(default=None)
    connector_tasks: Optional[int] = Field(default=None)


class Edge(BaseModel):
    source: str
    target: str


class Graph(BaseModel):
    directed: bool
    multigraph: bool
    graph: Any
    nodes: List[Node]
    edges: List[Edge]


class ReplicaCount(NamedTuple):
    ready: Optional[int]
    total: Optional[int]


class AppState(BaseModel):
    id: str
    state: str  # TODO: K8sReason
    replicas: ReplicaCount
