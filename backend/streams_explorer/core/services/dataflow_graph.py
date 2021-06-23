from typing import Dict, List, Optional, Set, Tuple, Type

import networkx as nx
from loguru import logger
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.generators.ego import ego_graph

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import ATTR_PIPELINE, K8sApp
from streams_explorer.core.services.metric_providers import MetricProvider
from streams_explorer.models.graph import Metric
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.node_types import NodeTypesEnum
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source

Node = Tuple[str, dict]
Edge = Tuple[str, str]


class NodeNotFound(Exception):
    pass


class DataFlowGraph:
    def __init__(self, metric_provider: Type[MetricProvider]):
        self.graph = nx.DiGraph()
        self.pipelines: Dict[str, nx.DiGraph] = {}
        self.metric_provider_class = metric_provider

    def add_streaming_app(self, app: K8sApp):
        pipeline = app.attributes.get(ATTR_PIPELINE)

        self._add_streaming_app(self.graph, app)
        if pipeline:
            self._add_streaming_app(
                self.pipelines.setdefault(pipeline, nx.DiGraph()), app
            )

    def _add_streaming_app(self, graph: nx.DiGraph, app: K8sApp):
        graph.add_node(
            app.name,
            label=app.name,
            node_type=NodeTypesEnum.STREAMING_APP,
            **app.attributes,
        )
        if app.output_topic:
            self._add_topic(graph, app.output_topic)
            self._add_output_topic(graph, app.name, app.output_topic)
        if app.error_topic:
            self._add_error_topic(graph, app.name, app.error_topic)
        for input_topic in app.input_topics:
            self._add_topic(graph, input_topic)
            self._add_input_topic(graph, app.name, input_topic)
        for extra_input in app.extra_input_topics:
            self._add_topic(graph, extra_input)
            self._add_input_topic(graph, app.name, extra_input)
        for extra_output in app.extra_output_topics:
            self._add_topic(graph, extra_output)
            self._add_output_topic(graph, app.name, extra_output)

    def add_connector(self, connector: KafkaConnector, pipeline: Optional[str] = None):
        graph = self.graph
        if pipeline is not None:
            graph = self.pipelines[pipeline]

        graph.add_node(
            connector.name,
            label=connector.name,
            node_type=NodeTypesEnum.CONNECTOR,
        )
        for topic in connector.topics:
            self._add_topic(graph, topic)
            if connector.type == KafkaConnectorTypesEnum.SINK:
                graph.add_edge(topic, connector.name)
            elif connector.type == KafkaConnectorTypesEnum.SOURCE:
                graph.add_edge(connector.name, topic)
        if connector.error_topic:
            self._add_error_topic(graph, connector.name, connector.error_topic)

        # Add to pipeline graph
        if pipeline is None:
            if pipelines := self.find_associated_pipelines(
                connector.name,
                reverse=connector.type == KafkaConnectorTypesEnum.SINK,
                radius=2,
            ):
                for pipeline in pipelines:
                    self.add_connector(connector, pipeline=pipeline)

    def add_source(self, source: Source):
        node = (source.name, {"label": source.name, "node_type": source.node_type})
        edge = (source.name, source.target)
        self.add_to_graph(node, edge)

    def add_sink(self, sink: Sink):
        node = (sink.name, {"label": sink.name, "node_type": sink.node_type})
        edge = (sink.source, sink.name)
        self.add_to_graph(node, edge, reverse=True)

    def add_to_graph(self, node: Node, edge: Edge, reverse=False):
        node_name, node_data = node
        self.graph.update(nodes=[node], edges=[edge])

        if pipelines := self.find_associated_pipelines(node_name, reverse=reverse):
            for pipeline in pipelines:
                # verify target exists in pipeline graph
                target = (set(edge) - {node_name}).pop()
                if not self.pipelines[pipeline].has_node(target):
                    logger.debug(
                        f"'{node_name}' doesn't belong to pipeline '{pipeline}', '{target}' is not a member of graph"
                    )
                    continue
                self.pipelines[pipeline].add_node(node_name, **node_data)
                self.pipelines[pipeline].add_edge(*edge)

    def get_positioned_pipeline_graph(self, pipeline_name: str) -> dict:
        return self.__get_positioned_json_graph(self.pipelines[pipeline_name])

    def get_positioned_graph(self) -> dict:
        return self.__get_positioned_json_graph(self.graph)

    def get_metrics(self) -> List[Metric]:
        if self.metric_provider is not None:
            return self.metric_provider.get()
        return []

    def get_node_type(self, id: str) -> str:
        try:
            return self.graph.nodes[id].get("node_type")
        except KeyError:
            raise NodeNotFound()

    def find_associated_pipelines(
        self, node_name: str, reverse: bool = False, radius: int = 3
    ) -> Set[str]:
        """
        Search neighborhood of connected successor nodes for pipeline label (used for sources).
        With reverse=True the neighborhood of predecessor nodes is searched instead (used for sinks).
        """
        graph = self.graph.reverse() if reverse else self.graph
        neighborhood = ego_graph(graph, node_name, radius=radius, undirected=False)
        pipelines = set()
        for _, node in neighborhood.nodes(data=True):
            if pipeline := node.get(ATTR_PIPELINE):
                logger.debug("Pipeline found for {}: {}", node_name, pipeline)
                pipelines.add(pipeline)
        if not pipelines:
            logger.warning("No pipeline found for {}", node_name)
        return pipelines

    @staticmethod
    def _add_topic(graph: nx.DiGraph, name: str):
        graph.add_node(name, label=name, node_type=NodeTypesEnum.TOPIC)

    @staticmethod
    def _add_input_topic(graph: nx.DiGraph, streaming_app: str, topic_name: str):
        graph.add_edge(topic_name, streaming_app)

    def _add_output_topic(
        self,
        graph: nx.DiGraph,
        streaming_app: str,
        topic_name: str,
    ):
        self._add_topic(graph, topic_name)
        graph.add_edge(streaming_app, topic_name)

    @staticmethod
    def _add_error_topic(
        graph: nx.DiGraph,
        streaming_app: str,
        topic_name: str,
    ):
        graph.add_node(
            topic_name,
            label=topic_name,
            node_type=NodeTypesEnum.ERROR_TOPIC,
        )
        graph.add_edge(streaming_app, topic_name)

    def reset(self):
        self.graph = nx.DiGraph()
        self.pipelines = {}
        self.metric_provider = self.metric_provider_class(self.graph.nodes(data=True))

    @staticmethod
    def __get_json_graph(graph: nx.Graph) -> dict:
        json_graph: dict = nx.node_link_data(graph)
        json_graph["edges"] = json_graph.pop("links")
        return json_graph

    @staticmethod
    def __get_positioned_json_graph(graph: nx.Graph) -> dict:
        pos = graphviz_layout(graph, prog="dot", args=settings.graph_layout_arguments)
        x = {n: p[0] for n, p in pos.items()}
        y = {n: p[1] for n, p in pos.items()}
        nx.set_node_attributes(graph, x, "x")
        nx.set_node_attributes(graph, y, "y")
        return DataFlowGraph.__get_json_graph(graph)
