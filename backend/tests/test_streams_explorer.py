from typing import List

import pytest
from kubernetes.client import V1beta1CronJob

from streams_explorer.core.config import settings
from streams_explorer.core.extractor.default.elasticsearch_sink import ElasticsearchSink
from streams_explorer.core.extractor.default.generic import GenericSink, GenericSource
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.core.k8s_app import K8sAppCronJob
from streams_explorer.core.services import schemaregistry
from streams_explorer.core.services.dataflow_graph import NodeTypesEnum
from streams_explorer.core.services.metric_providers import MetricProvider
from streams_explorer.defaultlinker import DefaultLinker
from streams_explorer.extractors import extractor_container
from streams_explorer.models.kafka_connector import KafkaConnectorTypesEnum
from streams_explorer.models.node_information import (
    NodeInfoListItem,
    NodeInformation,
    NodeInfoType,
)
from streams_explorer.models.source import Source
from streams_explorer.streams_explorer import StreamsExplorer
from tests.utils import get_streaming_app_cronjob, get_streaming_app_deployment


class TestStreamsExplorer:
    @pytest.fixture(autouse=True)
    def kafka_connect(self):
        settings.kafkaconnect.url = "testurl:3000"
        schemaregistry.url = "testurl:8000"

    @staticmethod
    def get_topic_value_schema(topic: str, version: int = 1) -> dict:
        if version == 1:
            return {
                "type": "record",
                "namespace": "com.test",
                "name": "Test1",
                "fields": [
                    {"name": "first", "type": "string"},
                ],
            }
        else:
            return {
                "type": "record",
                "namespace": "com.test",
                "name": "Test2",
                "fields": [
                    {"name": "first", "type": "string"},
                ],
            }

    @pytest.fixture()
    def deployments(self):
        return [
            get_streaming_app_deployment(
                "streaming-app1", "input-topic1", "output-topic1", "error-topic1"
            ),
            get_streaming_app_deployment(
                "streaming-app2",
                "input-topic2",
                "output-topic2",
                "error-topic2",
                consumer_group="consumer-group2",
            ),
            get_streaming_app_deployment(
                "streaming-app3",
                "input-topic3",
                "output-topic3",
                "error-topic3",
                pipeline="pipeline2",
            ),
        ]

    @pytest.fixture()
    def cron_jobs(self):
        return [get_streaming_app_cronjob()]

    @pytest.fixture()
    def fake_linker(self, mocker):
        """Creates LinkingService with non-default NodeInfoListItems."""

        def fake_linker_init(self):
            self.topic_info = [
                NodeInfoListItem(
                    name="Test Topic Monitoring", value="test", type=NodeInfoType.LINK
                ),
            ]

        mocker.patch(
            "streams_explorer.defaultlinker.DefaultLinker.__init__",
            fake_linker_init,
        )
        return DefaultLinker()

    @pytest.fixture()
    def streams_explorer(
        self, mocker, deployments, cron_jobs, monkeypatch, fake_linker
    ):
        explorer = StreamsExplorer(
            linking_service=fake_linker, metric_provider=MetricProvider
        )
        extractor_container.extractors = [
            ElasticsearchSink(),
            GenericSink(),
            GenericSource(),
        ]
        monkeypatch.setattr(settings.k8s, "consumer_group_annotation", "consumerGroup")
        mocker.patch.object(
            explorer, attribute="get_deployments", return_value=deployments
        )

        mocker.patch.object(explorer, attribute="get_stateful_sets", return_value=[])

        mocker.patch.object(explorer, attribute="get_cron_jobs", return_value=cron_jobs)

        def get_connectors():
            return ["es-sink-connector", "generic-source-connector"]

        def get_connector_info(connector):
            if connector == "es-sink-connector":
                return {
                    "config": {
                        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
                        "test": "test_value",
                        "topics": "output-topic1,output-topic2",
                        "errors.deadletterqueue.topic.name": "es-sink-connector-dead-letter-topic",
                    },
                    "type": KafkaConnectorTypesEnum.SINK,
                }
            if connector == "generic-source-connector":
                return {
                    "config": {
                        "connector.class": "GenericSourceConnector",
                        "name": "generic-source",
                    },
                    "type": KafkaConnectorTypesEnum.SOURCE,
                }

        def get_topic_value_schema_versions(topic: str) -> list:
            if topic == "es-sink-connector-dead-letter-topic":
                return []
            return [1, 2]

        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
            get_connectors,
        )
        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
            get_connector_info,
        )
        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.sanitize_connector_config",
            lambda config: config,
        )

        mocker.patch(
            "streams_explorer.core.services.schemaregistry.SchemaRegistry.get_topic_value_schema_versions",
            get_topic_value_schema_versions,
        )
        mocker.patch(
            "streams_explorer.core.services.schemaregistry.SchemaRegistry.get_topic_value_schema",
            self.get_topic_value_schema,
        )

        return explorer

    @pytest.mark.asyncio
    async def test_update(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()
        assert len(streams_explorer.applications) == 3
        assert len(streams_explorer.kafka_connectors) == 2

    @pytest.mark.asyncio
    async def test_get_pipeline_names(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()
        assert streams_explorer.get_pipeline_names() == [
            "pipeline2",
        ]

    @pytest.mark.asyncio
    async def test_get_node_information(
        self, streams_explorer: StreamsExplorer, monkeypatch
    ):
        await streams_explorer.update()
        monkeypatch.setattr(
            settings.kafkaconnect,
            "displayed_information",
            [{"name": "test", "key": "test"}],
        )
        monkeypatch.setattr(
            settings.k8s,
            "displayed_information",
            [{"name": "Test Label", "key": "metadata.labels.test_label"}],
        )

        assert streams_explorer.get_node_information(
            "streaming-app2"
        ) == NodeInformation(
            node_id="streaming-app2",
            node_type=NodeTypesEnum.STREAMING_APP,
            info=[],
        )
        assert streams_explorer.get_node_information("input-topic1") == NodeInformation(
            node_id="input-topic1",
            node_type=NodeTypesEnum.TOPIC,
            info=[
                NodeInfoListItem(
                    name="Test Topic Monitoring", value="test", type=NodeInfoType.LINK
                ),
                NodeInfoListItem(
                    name="Schema",
                    value=self.get_topic_value_schema("", 2),
                    type=NodeInfoType.JSON,
                ),
            ],
        )
        assert streams_explorer.get_node_information(
            "es-sink-connector"
        ) == NodeInformation(
            node_id="es-sink-connector",
            node_type=NodeTypesEnum.CONNECTOR,
            info=[
                NodeInfoListItem(
                    name="test", value="test_value", type=NodeInfoType.BASIC
                )
            ],
        )
        assert streams_explorer.get_node_information(
            "es-sink-connector-dead-letter-topic"
        ) == NodeInformation(
            node_id="es-sink-connector-dead-letter-topic",
            node_type=NodeTypesEnum.ERROR_TOPIC,
            info=[
                NodeInfoListItem(
                    name="Test Topic Monitoring", value="test", type=NodeInfoType.LINK
                ),
            ],
        )

        # clear topic_info
        streams_explorer.linking_service.topic_info = []
        assert streams_explorer.get_node_information(
            "es-sink-connector-dead-letter-topic"
        ) == NodeInformation(
            node_id="es-sink-connector-dead-letter-topic",
            node_type=NodeTypesEnum.ERROR_TOPIC,
            info=[],
        )

    @pytest.mark.asyncio
    async def test_cron_job_extractor(self, streams_explorer: StreamsExplorer):
        class MockCronjobExtractor(Extractor):
            def __init__(self):
                self.sources: List[Source] = []
                self.cron_job = None

            def on_cron_job_parsing(self, cron_job: V1beta1CronJob):
                self.cron_job = cron_job
                return K8sAppCronJob(cron_job)

        extractor = MockCronjobExtractor()
        extractor_container.extractors = [extractor]
        await streams_explorer.update()
        assert extractor.cron_job.metadata.name == "test-cronjob"
        assert "test-cronjob" in streams_explorer.applications
        extractor_container.extractors = []

    @pytest.mark.asyncio
    async def test_get_link_default(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()

        # topics
        assert type(streams_explorer.get_link("input-topic1", "grafana")) is str
        assert type(streams_explorer.get_link("input-topic1", "akhq")) is str

        # apps
        assert "consumergroups=consumer-group2" in streams_explorer.get_link(
            "streaming-app2", "grafana"
        )
        assert "/group/consumer-group2" in streams_explorer.get_link(
            "streaming-app2", "akhq"
        )

        # connectors
        assert streams_explorer.get_link("es-sink-connector", "grafana") is None
        assert streams_explorer.get_link("es-sink-connector", "akhq") is None
        assert "consumergroups=connect-generic-source" in streams_explorer.get_link(
            "generic-source-connector", "grafana"
        )
        assert "/group/connect-generic-source" in streams_explorer.get_link(
            "generic-source-connector", "akhq"
        )

        # sinks/sources
        assert "consumergroups=connect-generic-source" in streams_explorer.get_link(
            "generic-source-connector", "grafana"
        )

    @pytest.mark.asyncio
    async def test_get_link_kowl(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()

        # topics
        assert (
            streams_explorer.get_link("input-topic1", "kowl")
            == f"{settings.kowl.url}/topics/input-topic1"
        )

        # apps
        assert "/groups/consumer-group2" in streams_explorer.get_link(
            "streaming-app2", "kowl"
        )

        # connectors
        assert "/groups/connect-generic-source" in streams_explorer.get_link(
            "generic-source-connector", "kowl"
        )

    @pytest.mark.asyncio
    async def test_get_link_akhq(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()

        # topics
        assert (
            streams_explorer.get_link("input-topic1", "akhq")
            == f"{settings.akhq.url}/ui/kubernetes-cluster/topic/input-topic1"
        )

        # apps
        assert "/group/consumer-group2" in streams_explorer.get_link(
            "streaming-app2", "akhq"
        )

        # connectors
        assert "/group/connect-generic-source" in streams_explorer.get_link(
            "generic-source-connector", "akhq"
        )
        settings.akhq.connect = "kafka-connect"
        assert (
            "/kubernetes-cluster/connect/kafka-connect/definition/generic-source/tasks"
            in streams_explorer.get_link("generic-source-connector", "akhq-connect")
        )

    @pytest.mark.asyncio
    async def test_get_link_kibanalogs(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()
        assert (
            streams_explorer.get_link("streaming-app2", "kibanalogs")
            == f"{settings.kibanalogs.url}/app/discover#/?_a=(columns:!(message),query:(language:lucene,query:'kubernetes.labels.app: \"streaming-app2\"'))"
        )

    @pytest.mark.asyncio
    async def test_get_link_loki(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()
        assert (
            '/explore?orgId=1&left=["now-1h","now","loki",{"expr":"{app=\\"streaming-app2\\"}"}]'
            in streams_explorer.get_link("streaming-app2", "loki")
        )

    @pytest.mark.asyncio
    async def test_graph_caching(self, streams_explorer: StreamsExplorer):
        await streams_explorer.update()
        json_graph = streams_explorer.data_flow.json_graph
        assert json_graph
        assert len(json_graph["nodes"]) == 15
        assert len(json_graph["edges"]) == 12

        streams_explorer.data_flow.reset()
        assert not streams_explorer.data_flow.json_graph

    @pytest.mark.asyncio
    async def test_pipeline_graph_caching(
        self, mocker, streams_explorer: StreamsExplorer
    ):
        await streams_explorer.update()
        assert streams_explorer.data_flow.json_pipelines == {}

        calc_function = mocker.spy(
            streams_explorer.data_flow, "_DataFlowGraph__get_positioned_json_graph"
        )
        pipeline_graph = await streams_explorer.get_positioned_pipeline_json_graph(
            "pipeline2"
        )
        assert pipeline_graph
        assert len(pipeline_graph["nodes"]) == 4
        assert len(pipeline_graph["edges"]) == 3
        pipeline_graph = await streams_explorer.get_positioned_pipeline_json_graph(
            "pipeline2"
        )
        # verify caching works, pipeline graph is only calculated once
        calc_function.assert_called_once()

        streams_explorer.data_flow.reset()
        assert not streams_explorer.data_flow.json_pipelines
