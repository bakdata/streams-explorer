from typing import Any, NamedTuple

from pydantic import BaseModel, Field

from streams_explorer.models.k8s import K8sReason

GraphNode = tuple[str, dict]
GraphEdge = tuple[str, str]


class Node(BaseModel):
    id: str
    label: str
    node_type: str
    x: int | None = Field(default=None)
    y: int | None = Field(default=None)


class Metric(BaseModel):
    node_id: str
    messages_in: float | None = Field(default=None)
    messages_out: float | None = Field(default=None)
    consumer_lag: int | None = Field(default=None)
    consumer_read_rate: float | None = Field(default=None)
    topic_size: int | None = Field(default=None)
    replicas: int | None = Field(default=None)
    replicas_available: int | None = Field(default=None)
    connector_tasks: int | None = Field(default=None)


class Edge(BaseModel):
    source: str
    target: str


class Graph(BaseModel):
    directed: bool
    multigraph: bool
    graph: Any
    nodes: list[Node]
    edges: list[Edge]


class ReplicaCount(NamedTuple):
    ready: int | None
    total: int | None


class AppState(BaseModel):
    id: str
    state: K8sReason
    replicas: ReplicaCount
