from typing import Dict, List, Optional, Tuple

import networkx
from fastapi import FastAPI
from loguru import logger
from networkx import Graph
from networkx.drawing.nx_agraph import graphviz_layout

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.services.metric_providers import PrometheusMetricProvider
from streams_explorer.models.graph import Metric
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.node_types import NodeTypesEnum
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source


class NodeNotFound(Exception):
    pass


class DataFlowGraph:
    def __init__(self):
        self.graph = networkx.DiGraph()
        self.independent_graphs: Dict[str, networkx.DiGraph] = {}
        self.metrics_provider = PrometheusMetricProvider(self.graph.nodes(data=True))

    def add_streaming_app(self, app: K8sApp):
        self.graph.add_node(
            app.name,
            label=app.name,
            node_type=NodeTypesEnum.STREAMING_APP,
            labelPosition="bottom",
            **app.attributes,
        )
        self._add_topic(app.output_topic)
        self._add_output_topic(app.name, app.output_topic)
        if app.error_topic is not None:
            self._add_error_topic(app.name, app.error_topic)
        if app.input_topics is not None:
            for input_topic in app.input_topics:
                self._add_topic(input_topic)
                self._add_input_topic(app.name, input_topic)

        if app.extra_input_topics is not None:
            for extra_input in app.extra_input_topics:
                self._add_topic(extra_input)
                self._add_input_topic(app.name, extra_input)

        if app.extra_output_topics is not None:
            for extra_output in app.extra_output_topics:
                self._add_topic(extra_output)
                self._add_output_topic(app.name, extra_output)

    def add_connector(self, connector: KafkaConnector):
        self.graph.add_node(
            connector.name,
            label=connector.name,
            node_type=NodeTypesEnum.CONNECTOR,
            labelPosition="bottom",
        )
        for topic in connector.topics:
            self._add_topic(topic)
            self.graph.add_edge(topic, connector.name)

    def add_source(self, source: Source):
        self.graph.add_node(
            source.name,
            label=source.name,
            node_type=source.node_type,
            labelPosition="bottom",
        )
        self.graph.add_edge(source.name, source.target)

    def add_sink(self, sink: Sink):
        self.graph.add_node(
            sink.name,
            label=sink.name,
            node_type=sink.node_type,
            labelPosition="bottom",
        )
        self.graph.add_edge(sink.source, sink.name)

    def get_positioned_pipeline_graph(self, pipeline_name: str) -> dict:
        return self.__get_positioned_json_graph(self.independent_graphs[pipeline_name])

    def get_positioned_graph(self) -> dict:
        return self.__get_positioned_json_graph(self.graph)

    def get_metrics(self) -> List[Metric]:
        return self.metrics_provider.get()

    def get_node_type(self, id: str) -> str:
        try:
            return self.graph.nodes[id].get("node_type")
        except KeyError:
            raise NodeNotFound()

    def extract_independent_pipelines(self):
        undirected_graph = self.graph.to_undirected()
        independent_pipeline_nodes = list(
            networkx.connected_components(undirected_graph)
        )
        for pipeline in independent_pipeline_nodes:
            pipeline_graph = self.graph.subgraph(pipeline)
            pipeline_name = self.__extract_pipeline_name(pipeline_graph)
            self.independent_graphs[pipeline_name] = pipeline_graph

    def _add_topic(self, name):
        self.graph.add_node(
            name,
            label=name,
            node_type=NodeTypesEnum.TOPIC,
            labelPosition="bottom",
        )

    def _add_input_topic(self, streaming_app, topic_name):
        self.graph.add_edge(topic_name, streaming_app)

    def _add_output_topic(self, streaming_app, topic_name):
        self._add_topic(topic_name)
        self.graph.add_edge(streaming_app, topic_name)

    def _add_error_topic(self, streaming_app, topic_name):
        self.graph.add_node(
            topic_name,
            label=topic_name,
            node_type=NodeTypesEnum.ERROR_TOPIC,
            labelPosition="bottom",
        )
        self.graph.add_edge(streaming_app, topic_name)

    def __extract_pipeline_name(self, pipeline_graph):
        streaming_apps = list(
            filter(self.__filter_streaming_apps, pipeline_graph.nodes(data=True))
        )
        if len(streaming_apps) < 1:
            return list(pipeline_graph.nodes)[0]

        name = unique_name = self.__get_streaming_app_pipeline(streaming_apps[0])

        index = 0
        while self.independent_graphs.get(unique_name) is not None:
            index += 1
            unique_name = f"{name}{index}"
        return unique_name

    def reset(self):
        self.graph = networkx.DiGraph()
        self.independent_graphs = {}
        self.metrics_provider = PrometheusMetricProvider(self.graph.nodes(data=True))

    @staticmethod
    def __filter_streaming_apps(node: Tuple[str, dict]):
        node_type = node[1].get("node_type")
        return node_type is not None and node_type == NodeTypesEnum.STREAMING_APP

    @staticmethod
    def __get_streaming_app_pipeline(streaming_app) -> str:
        streaming_app_name, streaming_app_labels = streaming_app
        pipeline: Optional[str] = None
        if (
            settings.k8s.independent_graph
            and settings.k8s.independent_graph.label is not None
        ):
            pipeline = streaming_app_labels.get(settings.k8s.independent_graph.label)
        if pipeline is None:
            pipeline = streaming_app_name
        return pipeline

    @staticmethod
    def __get_json_graph(graph: Graph) -> dict:
        json_graph: dict = networkx.node_link_data(graph)
        json_graph["edges"] = json_graph.pop("links")
        return json_graph

    @staticmethod
    def __get_positioned_json_graph(graph: Graph) -> dict:
        pos = graphviz_layout(graph, prog="dot", args="-Grankdir=LR -Gnodesep=0.8")
        x = {n: p[0] for n, p in pos.items()}
        y = {n: p[1] for n, p in pos.items()}
        networkx.set_node_attributes(graph, x, "x")
        networkx.set_node_attributes(graph, y, "y")
        return DataFlowGraph.__get_json_graph(graph)


async def setup_dataflow_graph(app: FastAPI) -> None:
    logger.info("Setup dataflow graph")
    app.state.dataflow_graph = DataFlowGraph()
