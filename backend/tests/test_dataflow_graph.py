from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.services.dataflow_graph import DataFlowGraph
from streams_explorer.core.services.kafkaconnect import KafkaConnector
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source
from tests.utils import get_streaming_app_deployment


class TestDataFlowGraph:
    def test_add_streaming_app(self):
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app())

        assert len(df.graph.nodes) == 4
        assert df.graph.has_edge("input-topic", "test-app")
        assert df.graph.has_edge("test-app", "output-topic")
        assert df.graph.has_edge("test-app", "error-topic")

        # should have multiple input topic
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app(input_topics="input-topic1,input-topic2"))

        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("input-topic1", "test-app")
        assert df.graph.has_edge("input-topic2", "test-app")
        assert df.graph.has_edge("test-app", "output-topic")
        assert df.graph.has_edge("test-app", "error-topic")

        df = DataFlowGraph()
        df.add_streaming_app(
            self.get_k8s_app(multiple_outputs="1=extra-output1,2=extra-output2")
        )

        assert len(df.graph.nodes) == 6
        assert df.graph.has_edge("input-topic", "test-app")
        assert df.graph.has_edge("test-app", "output-topic")
        assert df.graph.has_edge("test-app", "error-topic")
        assert df.graph.has_edge("test-app", "extra-output1")
        assert df.graph.has_edge("test-app", "extra-output2")

    def test_add_connector(self):
        connector = KafkaConnector(
            name="test-connector", topics=["output-topic"], config={}
        )
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app())
        df.add_connector(connector)
        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("output-topic", "test-connector")

    def test_add_source(self):
        source = Source(
            name="test-source",
            node_type="test-type",
            target="test-app",
        )
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app())
        df.add_source(source)
        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("test-source", "test-app")

    def test_add_sink(self):
        sink = Sink(
            name="test-sink",
            node_type="test-type",
            source="test-app",
        )
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app())
        df.add_sink(sink)
        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("test-app", "test-sink")

    def test_get_positioned_json_graph(self):
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app())
        df.get_positioned_graph()
        nodes = df.graph.nodes(data=True)
        for _, data in nodes:
            assert data.get("x") is not None
            assert data.get("y") is not None

    def test_get_node_type(self):
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app())
        assert df.get_node_type("test-app") == "streaming-app"

    def test_node_attributes(self):
        df = DataFlowGraph()
        df.add_streaming_app(
            self.get_k8s_app(
                name="test-app1",
                pipeline="pipeline1",
            )
        )
        assert df.graph.nodes["test-app1"].get("pipeline") == "pipeline1"
        df.add_streaming_app(
            self.get_k8s_app(
                name="test-app2",
                pipeline=None,
            )
        )
        assert df.graph.nodes["test-app2"].get("pipeline") is None

    def test_extract_independent_pipelines(self):
        settings.k8s.independent_graph.label = "pipeline"
        df = DataFlowGraph()
        df.add_streaming_app(self.get_k8s_app())
        df.add_streaming_app(
            self.get_k8s_app(
                name="type2-app2",
                input_topics="input-topic2",
                error_topic="error-topic2",
                output_topic="output-topic2",
                pipeline="pipeline2",
            )
        )
        df.extract_independent_pipelines()
        assert "test-app" in df.independent_graphs
        assert "pipeline2" in df.independent_graphs

        df.graph.add_node("test-node")
        df.extract_independent_pipelines()
        assert "test-node" in df.independent_graphs

    @staticmethod
    def get_k8s_app(
        name="test-app",
        input_topics="input-topic",
        output_topic="output-topic",
        error_topic="error-topic",
        multiple_inputs=None,
        multiple_outputs=None,
        pipeline=None,
    ):
        return K8sApp(
            get_streaming_app_deployment(
                name,
                input_topics,
                output_topic,
                error_topic,
                multiple_inputs,
                multiple_outputs,
                pipeline=pipeline,
            )
        )
