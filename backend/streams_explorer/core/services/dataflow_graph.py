import re
from collections import defaultdict
from enum import Enum

import networkx as nx
from loguru import logger
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.generators.ego import ego_graph

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import ATTR_PIPELINE, K8sApp
from streams_explorer.core.services.kafka_admin_client import KafkaAdminClient
from streams_explorer.core.services.metric_providers import MetricProvider
from streams_explorer.models.graph import GraphEdge, GraphNode, Metric
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.node_types import NodeTypesEnum
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source


class NodeNotFound(Exception):
    pass


class PipelineNotFound(Exception):
    pass


class NodeDataFields(str, Enum):
    NODE_TYPE = "node_type"
    LABEL = "label"


class DataFlowGraph:
    def __init__(
        self, metric_provider: type[MetricProvider], kafka: KafkaAdminClient
    ) -> None:
        self.graph = nx.DiGraph()
        self.json_graph: dict = {}
        self.pipelines: dict[str, nx.DiGraph] = {}
        self.json_pipelines: dict[str, dict] = {}
        self.metric_provider_class = metric_provider
        self.metric_provider: MetricProvider | None = None
        self.kafka = kafka

        self._topic_pattern_queue: defaultdict[str, set[str]] = defaultdict(
            set
        )  # topic pattern -> set of target node ids

    async def store_json_graph(self) -> None:
        self.json_graph = await self.get_positioned_graph()

    def setup_metric_provider(self) -> None:
        self.metric_provider = self.metric_provider_class(
            list(self.graph.nodes(data=True))
        )

    def add_streaming_app(self, app: K8sApp) -> None:
        pipeline = app.attributes.get(ATTR_PIPELINE)

        self._add_streaming_app(self.graph, app)
        if pipeline:
            self._add_streaming_app(
                self.pipelines.setdefault(pipeline, nx.DiGraph()), app
            )

    def _add_streaming_app(self, graph: nx.DiGraph, app: K8sApp) -> None:
        graph.add_node(
            app.id,
            label=app.name,
            node_type=NodeTypesEnum.STREAMING_APP,
            **app.attributes,
        )

        for input_topic in app.input_topics:
            self._add_topic(graph, input_topic)
            self._add_input_topic(graph, app.id, input_topic)
        if app.output_topic:
            self._add_topic(graph, app.output_topic)
            self._add_output_topic(graph, app.id, app.output_topic)
        if app.error_topic:
            self._add_error_topic(graph, app.id, app.error_topic)
        if app.input_pattern:
            self._enqueue_input_pattern(app.input_pattern, app.id)
        for extra_input in app.extra_input_topics:
            self._add_topic(graph, extra_input)
            self._add_input_topic(graph, app.id, extra_input)
        for extra_output in app.extra_output_topics:
            self._add_topic(graph, extra_output)
            self._add_output_topic(graph, app.id, extra_output)
        for extra_pattern in app.extra_input_patterns:
            self._enqueue_input_pattern(extra_pattern, app.id)

    def add_connector(
        self, connector: KafkaConnector, pipeline: str | None = None
    ) -> None:
        graph = self.graph
        if pipeline is not None:
            graph = self.pipelines[pipeline]

        graph.add_node(
            connector.name,
            label=connector.name,
            node_type=NodeTypesEnum.CONNECTOR,
        )
        for topic in connector.get_topics():
            self._add_topic(graph, topic)
            if connector.type == KafkaConnectorTypesEnum.SINK:
                graph.add_edge(topic, connector.name)
            elif connector.type == KafkaConnectorTypesEnum.SOURCE:
                graph.add_edge(connector.name, topic)
        if connector_error_topic := connector.get_error_topic():
            self._add_error_topic(graph, connector.name, connector_error_topic)

        # Add to pipeline graph
        if pipeline is None:
            if pipelines := self.find_associated_pipelines(
                connector.name,
                reverse=connector.type == KafkaConnectorTypesEnum.SINK,
                radius=2,
            ):
                for pipeline in pipelines:
                    self.add_connector(connector, pipeline=pipeline)

    def add_source(self, source: Source) -> None:
        node: GraphNode = (
            source.name,
            {
                NodeDataFields.LABEL: source.name,
                NodeDataFields.NODE_TYPE: source.node_type,
            },
        )
        edge: GraphEdge = (source.name, source.target)
        self.add_to_graph(node, edge)

    def add_sink(self, sink: Sink) -> None:
        node: GraphNode = (
            sink.name,
            {NodeDataFields.LABEL: sink.name, NodeDataFields.NODE_TYPE: sink.node_type},
        )
        edge: GraphEdge = (sink.source, sink.name)
        self.add_to_graph(node, edge, reverse=True)

    def add_to_graph(
        self, node: GraphNode, edge: GraphEdge, reverse: bool = False
    ) -> None:
        node_name, node_data = node
        self.graph.update(nodes=[node], edges=[edge])

        if pipelines := self.find_associated_pipelines(node_name, reverse=reverse):
            target = (set(edge) - {node_name}).pop()
            for pipeline in pipelines:
                # verify target exists in pipeline graph
                if not self.pipelines[pipeline].has_node(target):
                    logger.debug(
                        f"'{node_name}' doesn't belong to pipeline '{pipeline}', '{target}' is not a member of graph"
                    )
                    continue
                self.pipelines[pipeline].add_node(node_name, **node_data)
                self.pipelines[pipeline].add_edge(*edge)

    async def get_positioned_pipeline_graph(self, pipeline_name: str) -> dict:
        if pipeline_name not in self.pipelines:
            raise PipelineNotFound()
        # caching
        if pipeline_name not in self.json_pipelines:
            self.json_pipelines[pipeline_name] = await self.__get_positioned_json_graph(
                self.pipelines[pipeline_name]
            )
        return self.json_pipelines[pipeline_name]

    async def get_positioned_graph(self) -> dict:
        return await self.__get_positioned_json_graph(self.graph)

    async def get_metrics(self) -> list[Metric]:
        if self.metric_provider is not None:
            return await self.metric_provider.get()
        return []

    def get_node_type(self, id: str) -> NodeTypesEnum:
        try:
            return self.graph.nodes[id][NodeDataFields.NODE_TYPE]
        except KeyError:
            raise NodeNotFound()

    def find_associated_pipelines(
        self, node_name: str, reverse: bool = False, radius: int = 3
    ) -> set[str]:
        """
        Search neighborhood of connected successor nodes for pipeline label (used for sources).
        With reverse=True the neighborhood of predecessor nodes is searched instead (used for sinks).
        """
        graph = self.graph.reverse() if reverse else self.graph
        neighborhood = ego_graph(graph, node_name, radius=radius, undirected=False)
        pipelines = set()
        for _, node in neighborhood.nodes(data=True):
            if pipeline := node.get(ATTR_PIPELINE):
                pipelines.add(pipeline)
        if pipelines:
            logger.debug("Pipelines found for {}: {}", node_name, pipelines)
        else:
            logger.warning("No pipeline found for {}", node_name)
        return pipelines

    @staticmethod
    def _add_topic(graph: nx.DiGraph, name: str) -> None:
        graph.add_node(name, label=name, node_type=NodeTypesEnum.TOPIC)

    @staticmethod
    def _filter_topic_node_ids(graph: nx.DiGraph) -> set[str]:
        return {
            node_id
            for node_id, data in graph.nodes(data=True)
            if data[  # pyright: ignore[reportOptionalSubscript]
                NodeDataFields.NODE_TYPE
            ]
            in (NodeTypesEnum.TOPIC, NodeTypesEnum.ERROR_TOPIC)
        }

    @staticmethod
    def _add_input_topic(graph: nx.DiGraph, app_id: str, topic_name: str) -> None:
        graph.add_edge(topic_name, app_id)

    def _add_output_topic(
        self,
        graph: nx.DiGraph,
        app_id: str,
        topic_name: str,
    ) -> None:
        self._add_topic(graph, topic_name)
        graph.add_edge(app_id, topic_name)

    def _enqueue_input_pattern(self, pattern: str, node_id: str) -> None:
        """
        Enqueue a input topic pattern for an app or Kafka Connector
        """
        self._topic_pattern_queue[pattern].add(node_id)

    def apply_input_pattern_edges(self) -> None:
        topics = DataFlowGraph._filter_topic_node_ids(self.graph)
        kafka_topics = self.kafka.get_all_topic_names() if self.kafka.enabled else set()
        for pattern, node_ids in self._topic_pattern_queue.items():
            regex = re.compile(pattern)
            matching_graph_known_topics = set(filter(regex.match, topics))
            # for unknown topics (unkown means not already present in the graph)
            # in the graph we have to create the topic node
            matching_unknown_kafka_topics = set(
                filter(regex.match, kafka_topics)
            ).difference(matching_graph_known_topics)
            for node_id in node_ids:  # node_id can be an app or a kafka connector
                pipeline = self.graph.nodes[node_id].get(ATTR_PIPELINE)
                # handle matching topics that are already present in the graph
                self.handle_matching_topics(
                    matching_graph_known_topics,
                    node_id,
                    pattern,
                    pipeline,
                    add_topic=False,
                )
                # handle unknown topics that are not present in the graph
                self.handle_matching_topics(
                    matching_unknown_kafka_topics,
                    node_id,
                    pattern,
                    pipeline,
                    add_topic=True,
                )

    def handle_matching_topics(
        self,
        matching_unknown_kafka_topics: set[str],
        node_id: str,
        pattern: str,
        pipeline: str | None,
        add_topic: bool = False,
    ) -> None:
        for matched_topic in matching_unknown_kafka_topics:
            if add_topic:
                self._add_topic(self.graph, matched_topic)
            if pipeline is not None:
                self.resolve_topic_pattern_in_pipeline(
                    matched_topic, node_id, pipeline, pattern
                )
            self.resolve_topic_pattern_in_all_graph(matched_topic, node_id, pattern)

    def resolve_topic_pattern_in_all_graph(
        self, matched_topic: str, node_id: str, pattern: str
    ) -> None:
        # resolve topic pattern in overall graph containing all pipelines
        if settings.graph.resolve.input_pattern_topics.all:
            # connect topic to graph
            self.graph.add_edge(matched_topic, node_id)
        else:
            self.add_pattern_as_topic(self.graph, node_id, pattern)

    def add_pattern_as_topic(
        self, graph: nx.DiGraph, node_id: str, pattern: str
    ) -> None:
        # visualize the pattern as topic
        self._add_topic(graph, pattern)
        graph.add_edge(pattern, node_id)

    def resolve_topic_pattern_in_pipeline(
        self, matched_topic: str, node_id: str, pipeline: str, pattern: str
    ) -> None:
        # resolve topic patterns in pipelines
        if settings.graph.resolve.input_pattern_topics.pipelines:
            if matched_topic not in self.pipelines[pipeline].nodes:
                node = self.graph.nodes[matched_topic]
                self.pipelines[pipeline].add_node(matched_topic, **node)
            self.pipelines[pipeline].add_edge(matched_topic, node_id)
        else:
            self.add_pattern_as_topic(self.pipelines[pipeline], node_id, pattern)

    @staticmethod
    def _add_error_topic(
        graph: nx.DiGraph,
        app_id: str,
        topic_name: str,
    ) -> None:
        graph.add_node(
            topic_name,
            **{
                NodeDataFields.LABEL: topic_name,
                NodeDataFields.NODE_TYPE: NodeTypesEnum.ERROR_TOPIC,
            },
        )
        graph.add_edge(app_id, topic_name)

    def reset(self) -> None:
        self.graph.clear()
        self.json_graph.clear()
        self.pipelines.clear()
        self.json_pipelines.clear()

    @staticmethod
    def __get_json_graph(graph: nx.Graph) -> dict:
        json_graph: dict = nx.node_link_data(graph)
        json_graph["edges"] = json_graph.pop("links")
        return json_graph

    @staticmethod
    def __extract_independent_graph_components(graph: nx.Graph) -> list[nx.Graph]:
        independent_graphs = list(nx.connected_components(graph.to_undirected()))
        subgraphs: list[nx.Graph] = []
        for pipeline in independent_graphs:
            subgraph: nx.Graph = graph.subgraph(pipeline)
            subgraphs.append(subgraph)
        return subgraphs

    @staticmethod
    async def __get_positioned_json_graph(graph: nx.Graph) -> dict:
        subgraphs = DataFlowGraph.__extract_independent_graph_components(graph)
        pos = graphviz_layout(graph, prog="dot", args=settings.graph.layout_arguments)
        x = {n: p[0] for n, p in pos.items()}
        y = {n: p[1] for n, p in pos.items()}
        nx.set_node_attributes(graph, x, "x")
        nx.set_node_attributes(graph, y, "y")
        for i, subgraph in enumerate(subgraphs):
            offset = i * settings.graph.pipeline_distance
            for node_name in list(subgraph.nodes):
                graph.nodes[node_name]["y"] += offset
        return DataFlowGraph.__get_json_graph(graph)
