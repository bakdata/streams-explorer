from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Type, cast

import networkx as nx
from loguru import logger
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.generators.ego import ego_graph

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.services.metric_providers import MetricProvider
from streams_explorer.models.graph import Metric
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.node_types import NodeTypesEnum
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source


class NodeNotFound(Exception):
    pass


class DataFlowGraph:
    def __init__(self, metric_provider: Type[MetricProvider]):
        self.graph = nx.DiGraph()
        self.pipelines: Dict[str, nx.DiGraph] = {}
        self.metric_provider_class = metric_provider

    def add_streaming_app(self, app: K8sApp):
        self.graph.add_node(
            app.name,
            label=app.name,
            node_type=NodeTypesEnum.STREAMING_APP,
            **app.attributes,
        )
        pipeline = app.attributes.get("pipeline")
        if app.output_topic:
            self._add_topic(app.output_topic, pipeline)
            self._add_output_topic(app.name, app.output_topic, pipeline)
        if app.error_topic:
            self._add_error_topic(app.name, app.error_topic, pipeline)
        for input_topic in app.input_topics:
            self._add_topic(input_topic, pipeline)
            self._add_input_topic(app.name, input_topic)
        for extra_input in app.extra_input_topics:
            self._add_topic(extra_input, pipeline)
            self._add_input_topic(app.name, extra_input)
        for extra_output in app.extra_output_topics:
            self._add_topic(extra_output, pipeline)
            self._add_output_topic(app.name, extra_output, pipeline)

    def add_connector(self, connector: KafkaConnector):
        self.graph.add_node(
            connector.name,
            label=connector.name,
            node_type=NodeTypesEnum.CONNECTOR,
        )
        for topic in connector.topics:
            self._add_topic(topic)
            if connector.type == KafkaConnectorTypesEnum.SINK:
                self.graph.add_edge(topic, connector.name)
            if connector.type == KafkaConnectorTypesEnum.SOURCE:
                self.graph.add_edge(connector.name, topic)
        if connector.error_topic:
            self._add_error_topic(connector.name, connector.error_topic)

    def add_source(self, source: Source):
        self.graph.add_node(
            source.name,
            label=source.name,
            node_type=source.node_type,
        )
        self.graph.add_edge(source.name, source.target)

    def add_sink(self, sink: Sink):
        self.graph.add_node(
            sink.name,
            label=sink.name,
            node_type=sink.node_type,
        )
        self.graph.add_edge(sink.source, sink.name)

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

    def extract_independent_pipelines(self):
        undirected_graph = self.graph.to_undirected()
        nodes = list(undirected_graph.nodes(data=True))
        # fix for networkx always reporting EdgeView tuple size 3 when it should be 2 for data=False
        edges = [cast(Tuple[str, str], edge) for edge in self.graph.edges()]

        # sort nodes by pipeline
        pipeline_nodes = defaultdict(list)
        for current_node in list(filter(self.__filter_pipeline_nodes, nodes)):
            pipeline_nodes[current_node[1]["pipeline"]].append(current_node)

        # assign pipeline for nodes without label
        for connector, _ in list(
            filter(lambda node: not self.__filter_pipeline_nodes(node), nodes)
        ):
            neighborhood = ego_graph(
                undirected_graph, connector, radius=3, undirected=True
            ).nodes(data=True)
            pipeline = None
            for _, node in neighborhood:
                pipeline = node.get("pipeline")
                if pipeline is not None:
                    logger.debug("Pipeline found for {}: {}", connector, pipeline)
                    pipeline_nodes[pipeline].extend(neighborhood)
                    break
            if pipeline is None:
                logger.warning("No pipeline found for {}", connector)

        # build pipeline graphs
        for pipeline, nodes in pipeline_nodes.items():
            graph = nx.DiGraph()
            graph.add_nodes_from(nodes)
            self.pipelines[pipeline] = graph

            # find edges belonging to pipeline
            node_names = [name for name, _ in nodes]
            for source, target in list(
                filter(
                    lambda edge: self.__filter_pipeline_edges(edge, node_names), edges
                )
            ):
                graph.add_edge(source, target)

    def _add_topic(self, name: str, pipeline: Optional[str] = None):
        self.graph.add_node(
            name, label=name, node_type=NodeTypesEnum.TOPIC, pipeline=pipeline
        )

    def _add_input_topic(
        self,
        streaming_app: str,
        topic_name: str,
    ):
        self.graph.add_edge(topic_name, streaming_app)

    def _add_output_topic(
        self, streaming_app: str, topic_name: str, pipeline: Optional[str] = None
    ):
        self._add_topic(topic_name, pipeline=pipeline)
        self.graph.add_edge(streaming_app, topic_name)

    def _add_error_topic(
        self, streaming_app: str, topic_name: str, pipeline: Optional[str] = None
    ):
        self.graph.add_node(
            topic_name,
            label=topic_name,
            node_type=NodeTypesEnum.ERROR_TOPIC,
            pipeline=pipeline,
        )
        self.graph.add_edge(streaming_app, topic_name)

    def reset(self):
        self.graph = nx.DiGraph()
        self.pipelines = {}
        self.metric_provider = self.metric_provider_class(self.graph.nodes(data=True))

    @staticmethod
    def __filter_pipeline_nodes(node: Tuple[str, dict]) -> bool:
        return node[1].get("pipeline") is not None

    @staticmethod
    def __filter_pipeline_edges(edge: Tuple[str, str], nodes: List[str]) -> bool:
        source, target = edge
        return source in nodes and target in nodes

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
