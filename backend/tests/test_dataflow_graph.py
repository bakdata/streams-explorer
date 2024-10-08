import pytest
from pytest import MonkeyPatch

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import ATTR_PIPELINE, K8sApp
from streams_explorer.core.services.dataflow_graph import (
    DataFlowGraph,
    PipelineNotFound,
)
from streams_explorer.core.services.kafka_admin_client import KafkaAdminClient
from streams_explorer.core.services.metric_providers import MetricProvider
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorConfig,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink
from streams_explorer.models.source import Source
from tests.utils import get_streaming_app_cronjob, get_streaming_app_deployment

settings.k8s.pipeline.label = "pipeline"


class TestDataFlowGraph:
    @pytest.fixture()
    def df(self) -> DataFlowGraph:
        return DataFlowGraph(metric_provider=MetricProvider, kafka=KafkaAdminClient())

    @pytest.mark.asyncio
    async def test_metric_provider_before_setup(self, df: DataFlowGraph):
        assert await df.get_metrics() == []

    @pytest.mark.asyncio
    async def test_positioned_pipeline_graph_not_found(self, df: DataFlowGraph):
        with pytest.raises(PipelineNotFound):
            await df.get_positioned_pipeline_graph("doesnt-exist")

    def test_add_streaming_app(self, df: DataFlowGraph):
        df.add_streaming_app(K8sApp.factory(get_streaming_app_deployment()))

        assert len(df.graph.nodes) == 4
        assert df.graph.has_edge("input-topic", "test-namespace/test-app")
        assert df.graph.has_edge("test-namespace/test-app", "output-topic")
        assert df.graph.has_edge("test-namespace/test-app", "error-topic")

        # should have multiple input topic
        df.reset()
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(input_topics="input-topic1,input-topic2")
            )
        )

        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("input-topic1", "test-namespace/test-app")
        assert df.graph.has_edge("input-topic2", "test-namespace/test-app")
        assert df.graph.has_edge("test-namespace/test-app", "output-topic")
        assert df.graph.has_edge("test-namespace/test-app", "error-topic")

        df.reset()
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    multiple_outputs="1=extra-output1,2=extra-output2"
                )
            )
        )

        assert len(df.graph.nodes) == 6
        assert df.graph.has_edge("input-topic", "test-namespace/test-app")
        assert df.graph.has_edge("test-namespace/test-app", "output-topic")
        assert df.graph.has_edge("test-namespace/test-app", "error-topic")
        assert df.graph.has_edge("test-namespace/test-app", "extra-output1")
        assert df.graph.has_edge("test-namespace/test-app", "extra-output2")

    def test_duplicate_node_names(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    namespace="test-namespace1", pipeline="pipeline1"
                )
            )
        )
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    namespace="test-namespace2", pipeline="pipeline2"
                )
            )
        )
        assert len(df.graph.nodes) == 5
        assert df.graph.has_node("test-namespace1/test-app")
        assert df.graph.has_node("test-namespace2/test-app")

        with pytest.raises(ValueError, match="Duplicate app test-namespace1/test-app"):
            df.add_streaming_app(
                K8sApp.factory(
                    get_streaming_app_deployment(
                        namespace="test-namespace1", pipeline="pipeline1"
                    )
                )
            )

    def test_resolve_input_pattern(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(error_topic="fake-dead-letter-topic")
            )
        )

        assert len(df.graph.nodes) == 4

        settings.graph.resolve.input_pattern_topics.all = True
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics=None,
                    output_topic="output-topic2",
                    error_topic="fake2-dead-letter-topic",
                    input_pattern=".*-dead-letter-topic",
                )
            )
        )
        df.apply_input_pattern_edges()
        assert len(df.graph.nodes) == 7
        assert df.graph.has_edge("fake-dead-letter-topic", "test-namespace/test-app2")
        assert df.graph.has_edge(
            "fake2-dead-letter-topic", "test-namespace/test-app2"
        ), "Should match on app's own error topic"
        assert df.graph.has_edge("test-namespace/test-app2", "output-topic2")
        assert df.graph.has_edge("test-namespace/test-app2", "fake2-dead-letter-topic")

    def test_resolve_input_patterns_for_topics_in_kafka(self, monkeypatch: MonkeyPatch):
        kafka = KafkaAdminClient()
        kafka._enabled = True

        def get_all_topic_names() -> set[str]:
            return {"another-dead-letter-topic", "another-non-matching-topic"}

        monkeypatch.setattr(kafka, "get_all_topic_names", get_all_topic_names)
        df = DataFlowGraph(metric_provider=MetricProvider, kafka=kafka)

        settings.graph.resolve.input_pattern_topics.all = True
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics=None,
                    output_topic="output-topic2",
                    error_topic="fake2-dead-letter-topic",
                    input_pattern=".*-dead-letter-topic",
                )
            )
        )
        df.apply_input_pattern_edges()
        assert len(df.graph.nodes) == 4
        assert df.graph.has_edge(
            "another-dead-letter-topic", "test-namespace/test-app2"
        )
        assert df.graph.has_edge("fake2-dead-letter-topic", "test-namespace/test-app2")
        assert df.graph.has_node("another-dead-letter-topic")
        assert not df.graph.has_node("another-non-matching-topic")

    def test_no_resolve_input_pattern(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(error_topic="fake-dead-letter-topic")
            )
        )

        assert len(df.graph.nodes) == 4

        settings.graph.resolve.input_pattern_topics.all = False
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics=None,
                    output_topic="output-topic2",
                    error_topic="fake2-dead-letter-topic",
                    input_pattern=".*-dead-letter-topic",
                )
            )
        )
        df.apply_input_pattern_edges()
        assert len(df.graph.nodes) == 8
        assert df.graph.has_edge(".*-dead-letter-topic", "test-namespace/test-app2")
        assert not df.graph.has_edge(
            "fake2-dead-letter-topic", "test-namespace/test-app2"
        )
        assert df.graph.has_edge("test-namespace/test-app2", "output-topic2")
        assert df.graph.has_edge("test-namespace/test-app2", "fake2-dead-letter-topic")

    def test_resolve_labeled_input_patterns(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    multiple_outputs="out=output-non-match-topic",
                    error_topic="fake-dead-letter-topic",
                )
            )
        )

        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("input-topic", "test-namespace/test-app")
        assert df.graph.has_edge("test-namespace/test-app", "output-topic")
        assert df.graph.has_edge("test-namespace/test-app", "fake-dead-letter-topic")

        settings.graph.resolve.input_pattern_topics.all = True
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics="output-topic",
                    output_topic="another-topic",
                    error_topic="fake2-dead-letter-topic",
                    labeled_input_patterns="fake1=.*-dead-letter-topic,fake2=.*-output-topic",
                )
            )
        )
        df.apply_input_pattern_edges()
        assert len(df.graph.nodes) == 8
        assert df.graph.has_edge("fake-dead-letter-topic", "test-namespace/test-app2")
        assert df.graph.has_edge(
            "fake2-dead-letter-topic", "test-namespace/test-app2"
        ), "Should match on app's own error topic"
        assert not df.graph.has_edge("another-topic", "test-namespace/test-app2")
        assert df.graph.has_edge("fake-dead-letter-topic", "test-namespace/test-app2")

    def test_no_resolve_labeled_input_patterns(self, df: DataFlowGraph):
        settings.graph.resolve.input_pattern_topics.all = False
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    multiple_outputs="out=output-non-match-topic",
                    error_topic="fake-dead-letter-topic",
                )
            )
        )

        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics="output-topic",
                    output_topic="output-topic2",
                    error_topic="fake2-dead-letter-topic",
                    labeled_input_patterns="fake1=.*-dead-letter-topic,fake2=.*output-topic",
                )
            )
        )
        df.apply_input_pattern_edges()
        assert len(df.graph.nodes) == 10
        assert df.graph.has_edge(".*-dead-letter-topic", "test-namespace/test-app2")
        assert df.graph.has_edge(".*output-topic", "test-namespace/test-app2")

    def test_add_connector(self, df: DataFlowGraph):
        sink_connector = KafkaConnector(
            name="test-sink-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(topics="output-topic"),
            error_topic="dead-letter-topic",
        )
        source_connector = KafkaConnector(
            name="test-source-connector",
            type=KafkaConnectorTypesEnum.SOURCE,
            config=KafkaConnectorConfig(topics="input-topic,input-topic2"),
        )
        df.add_streaming_app(K8sApp.factory(get_streaming_app_deployment()))
        df.add_connector(sink_connector)
        df.add_connector(source_connector)
        assert len(df.graph.nodes) == 8
        assert df.graph.has_edge("output-topic", "test-sink-connector")
        assert df.graph.has_edge("test-sink-connector", "dead-letter-topic")
        assert df.graph.has_edge("test-source-connector", "input-topic")
        assert df.graph.has_edge("test-source-connector", "input-topic2")
        assert len(df.pipelines) == 0

    def test_deprecated_connector(self, df: DataFlowGraph):
        sink_connector = KafkaConnector(
            name="test-sink-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(topics="output-topic"),
            error_topic="dead-letter-topic",
            topics=["output-topic"],
        )
        source_connector = KafkaConnector(
            name="test-source-connector",
            type=KafkaConnectorTypesEnum.SOURCE,
            config=KafkaConnectorConfig(topics="input-topic,input-topic2"),
            topics=["input-topic", "input-topic2"],
        )

        df.add_streaming_app(K8sApp.factory(get_streaming_app_deployment()))
        df.add_connector(sink_connector)
        df.add_connector(source_connector)
        assert len(df.graph.nodes) == 8
        assert df.graph.has_edge("output-topic", "test-sink-connector")
        assert df.graph.has_edge("test-sink-connector", "dead-letter-topic")
        assert df.graph.has_edge("test-source-connector", "input-topic")
        assert df.graph.has_edge("test-source-connector", "input-topic2")
        assert len(df.pipelines) == 0

    def test_add_source(self, df: DataFlowGraph):
        source = Source(
            name="test-source",
            node_type="test-type",
            target="test-namespace/test-app",
        )
        df.add_streaming_app(K8sApp.factory(get_streaming_app_deployment()))
        df.add_source(source)
        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("test-source", "test-namespace/test-app")
        assert len(df.pipelines) == 0

    def test_add_sink(self, df: DataFlowGraph):
        sink = Sink(
            name="test-sink",
            node_type="test-type",
            source="test-namespace/test-app",
        )
        df.add_streaming_app(K8sApp.factory(get_streaming_app_deployment()))
        df.add_sink(sink)
        assert len(df.graph.nodes) == 5
        assert df.graph.has_edge("test-namespace/test-app", "test-sink")
        assert len(df.pipelines) == 0

    @pytest.mark.asyncio
    async def test_get_positioned_json_graph(self, df: DataFlowGraph):
        df.add_streaming_app(K8sApp.factory(get_streaming_app_deployment()))
        await df.get_positioned_graph()
        nodes = df.graph.nodes(data=True)
        for _, data in iter(nodes):
            assert data is not None
            assert data.get("x") is not None
            assert data.get("y") is not None

    def test_get_node_type(self, df: DataFlowGraph):
        df.add_streaming_app(K8sApp.factory(get_streaming_app_deployment()))
        assert df.get_node_type("test-namespace/test-app") == "streaming-app"

    def test_node_attributes(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app1",
                    pipeline="pipeline1",
                )
            )
        )
        assert (
            df.graph.nodes["test-namespace/test-app1"].get(ATTR_PIPELINE) == "pipeline1"
        )
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    pipeline=None,
                )
            )
        )
        assert df.graph.nodes["test-namespace/test-app2"].get(ATTR_PIPELINE) is None

    def test_pipeline_graph(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    pipeline="pipeline1",
                )
            )
        )
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics="input-topic2",
                    error_topic="error-topic2",
                    output_topic="output-topic2",
                    pipeline="pipeline2",
                    multiple_inputs="0=output-topic",
                )
            )
        )
        assert len(df.pipelines) == 2
        assert "pipeline1" in df.pipelines
        assert "pipeline2" in df.pipelines
        pipeline1 = df.pipelines["pipeline1"]
        pipeline2 = df.pipelines["pipeline2"]
        assert set(pipeline1.nodes) == {
            "input-topic",
            "output-topic",
            "test-namespace/test-app",
            "error-topic",
        }
        assert set(pipeline2.nodes) == {
            "output-topic",
            "input-topic2",
            "output-topic2",
            "test-namespace/test-app2",
            "error-topic2",
        }

        df.add_sink(Sink("test-sink", "output-topic"))
        assert "test-sink" in pipeline1.nodes

        source_connector = KafkaConnector(
            name="test-source-connector",
            type=KafkaConnectorTypesEnum.SOURCE,
            config=KafkaConnectorConfig(topics="input-topic2,source-topic"),
        )
        df.add_connector(source_connector)
        assert "test-source-connector" in pipeline2.nodes
        assert "source-topic" in pipeline2.nodes

    def test_pipeline_cronjob(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_cronjob(
                    error_topic=None,
                    pipeline="pipeline1",
                )
            )
        )
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    input_topics="output-topic",
                    error_topic=None,
                    output_topic="output-topic2",
                    pipeline="pipeline1",
                )
            )
        )
        assert len(df.pipelines) == 1
        assert "pipeline1" in df.pipelines
        pipeline1 = df.pipelines["pipeline1"]
        assert set(pipeline1.nodes) == {
            "test-namespace/test-cronjob",
            "output-topic",
            "test-namespace/test-app",
            "output-topic2",
        }

    def test_multiple_pipelines_sink_source(self, df: DataFlowGraph):
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app1",
                    input_topics="input-topic1",
                    error_topic="error-topic1",
                    output_topic="output-topic1",
                    pipeline="pipeline1",
                )
            )
        )
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics="input-topic2",
                    error_topic="error-topic2",
                    output_topic="output-topic2",
                    pipeline="pipeline2",
                )
            )
        )
        assert len(df.pipelines) == 2
        assert "pipeline1" in df.pipelines
        assert "pipeline2" in df.pipelines
        pipeline1 = df.pipelines["pipeline1"]
        pipeline2 = df.pipelines["pipeline2"]
        assert set(pipeline1.nodes) == {
            "test-namespace/test-app1",
            "input-topic1",
            "output-topic1",
            "error-topic1",
        }
        assert set(pipeline2.nodes) == {
            "test-namespace/test-app2",
            "input-topic2",
            "output-topic2",
            "error-topic2",
        }

        sink_connector = KafkaConnector(
            name="test-sink-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(topics="output-topic1,output-topic2"),
        )
        df.add_connector(sink_connector)
        assert "test-sink-connector" in df.graph.nodes
        assert "test-sink-connector" in pipeline1.nodes
        assert "test-sink-connector" in pipeline2.nodes

        df.add_sink(Sink("test-sink", "test-sink-connector"))
        assert "test-sink" in df.graph.nodes
        assert "test-sink" in pipeline1.nodes
        assert "test-sink" in pipeline2.nodes

        source_connector = KafkaConnector(
            name="test-source-connector",
            type=KafkaConnectorTypesEnum.SOURCE,
            config=KafkaConnectorConfig(topics="input-topic1,input-topic2"),
        )
        df.add_connector(source_connector)
        assert "test-source-connector" in df.graph.nodes
        assert "test-source-connector" in pipeline1.nodes
        assert "test-source-connector" in pipeline2.nodes

        df.add_source(Source("test-source", "test-source-connector"))
        assert "test-source" in df.graph.nodes
        assert "test-source" in pipeline1.nodes
        assert "test-source" in pipeline2.nodes

        unrelated_sink_connector = KafkaConnector(
            name="unrelated-sink-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(topics="input-topic1"),
        )
        df.add_connector(unrelated_sink_connector)
        assert "unrelated-sink-connector" in df.graph.nodes
        assert "unrelated-sink-connector" not in pipeline1.nodes
        assert "unrelated-sink-connector" not in pipeline2.nodes

        unrelated_source_connector = KafkaConnector(
            name="unrelated-source-connector",
            type=KafkaConnectorTypesEnum.SOURCE,
            config=KafkaConnectorConfig(topics="output-topic1"),
        )
        df.add_connector(unrelated_source_connector)
        assert "unrelated-source-connector" in df.graph.nodes
        assert "unrelated-source-connector" not in pipeline1.nodes
        assert "unrelated-source-connector" not in pipeline2.nodes

    def test_verify_connector_exists_in_pipeline(self, df: DataFlowGraph):
        """Verify that connector exists in specific pipeline before adding it from a sink or source."""
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app1",
                    input_topics="input-topic1",
                    error_topic=None,
                    output_topic="output-topic1",
                    pipeline="pipeline1",
                )
            )
        )
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics="input-topic2",
                    error_topic=None,
                    output_topic="output-topic2",
                    pipeline="pipeline2",
                )
            )
        )
        sink_connector1 = KafkaConnector(
            name="sink-connector1",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(topics="output-topic1"),
        )
        df.add_connector(sink_connector1)
        sink_connector2 = KafkaConnector(
            name="sink-connector2",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(topics="output-topic2"),
        )
        df.add_connector(sink_connector2)

        sink = Sink(
            name="test-sink",
            node_type="test-type",
            source="sink-connector1",
        )
        df.add_sink(sink)
        sink.source = "sink-connector2"
        df.add_sink(sink)

        assert len(df.pipelines) == 2
        assert "pipeline1" in df.pipelines
        assert "pipeline2" in df.pipelines
        pipeline1 = df.pipelines["pipeline1"]
        pipeline2 = df.pipelines["pipeline2"]
        assert "sink-connector1" in pipeline1.nodes
        assert "sink-connector1" not in pipeline2.nodes
        assert "sink-connector2" in pipeline2.nodes
        assert "sink-connector2" not in pipeline1.nodes
        assert "test-sink" in pipeline1.nodes
        assert "test-sink" in pipeline2.nodes
        assert set(pipeline1.nodes) == {
            "test-namespace/test-app1",
            "input-topic1",
            "output-topic1",
            "sink-connector1",
            "test-sink",
        }
        assert set(pipeline2.nodes) == {
            "test-namespace/test-app2",
            "input-topic2",
            "output-topic2",
            "sink-connector2",
            "test-sink",
        }

    def test_multiple_pipelines_apps(self, df: DataFlowGraph):
        """Ensures apps have separate pipelines despite them being connected."""
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app1",
                    input_topics="input-topic1",
                    error_topic=None,
                    output_topic="output-topic1",
                    pipeline="pipeline1",
                )
            )
        )
        df.add_streaming_app(
            K8sApp.factory(
                get_streaming_app_deployment(
                    name="test-app2",
                    input_topics="output-topic1",
                    error_topic=None,
                    output_topic="output-topic2",
                    pipeline="pipeline2",
                )
            )
        )
        assert len(df.pipelines) == 2
        assert "pipeline1" in df.pipelines
        assert "pipeline2" in df.pipelines
        pipeline1 = df.pipelines["pipeline1"]
        pipeline2 = df.pipelines["pipeline2"]
        assert set(pipeline1.nodes) == {
            "test-namespace/test-app1",
            "input-topic1",
            "output-topic1",
        }
        assert set(pipeline2.nodes) == {
            "test-namespace/test-app2",
            "output-topic1",
            "output-topic2",
        }

    @pytest.mark.asyncio
    async def test_positioned_graph_distance(self, df: DataFlowGraph):
        settings.graph.pipeline_distance = 0
        df.graph.add_node("a1")
        df.graph.add_node("a2")
        df.graph.add_node("a3")
        df.graph.add_edge("a1", "a2")
        df.graph.add_edge("a2", "a3")
        df.graph.add_node("b1")
        df.graph.add_node("b2")
        df.graph.add_node("b3")
        df.graph.add_edge("b1", "b2")
        df.graph.add_edge("b2", "b3")

        async def nodes():
            graph = await df.get_positioned_graph()
            return graph["nodes"]

        assert await nodes() == [
            {"id": "a1", "x": 27.0, "y": 18.0},
            {"id": "a2", "x": 117.0, "y": 18.0},
            {"id": "a3", "x": 207.0, "y": 18.0},
            {"id": "b1", "x": 27.0, "y": 112.0},
            {"id": "b2", "x": 117.0, "y": 112.0},
            {"id": "b3", "x": 207.0, "y": 112.0},
        ]

        settings.graph.pipeline_distance = 500
        assert await nodes() == [
            {"id": "a1", "x": 27.0, "y": 18.0},
            {"id": "a2", "x": 117.0, "y": 18.0},
            {"id": "a3", "x": 207.0, "y": 18.0},
            {"id": "b1", "x": 27.0, "y": 612.0},
            {"id": "b2", "x": 117.0, "y": 612.0},
            {"id": "b3", "x": 207.0, "y": 612.0},
        ]
