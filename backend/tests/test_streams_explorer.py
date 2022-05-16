from typing import Optional, Set

import pytest
from kubernetes_asyncio.client import V1beta1CronJob

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
from streams_explorer.models.k8s_config import K8sConfig
from streams_explorer.models.kafka_connector import KafkaConnectorTypesEnum
from streams_explorer.models.node_information import (
    NodeInfoListItem,
    NodeInformation,
    NodeInfoType,
)
from streams_explorer.models.source import Source
from streams_explorer.streams_explorer import K8sDeploymentEvent, StreamsExplorer
from tests.utils import get_streaming_app_cronjob, get_streaming_app_deployment

APP1 = get_streaming_app_deployment(
    "streaming-app1", "input-topic1", "output-topic1", "error-topic1"
)


class TestStreamsExplorer:
    @pytest.fixture(autouse=True)
    def kafka_connect(self):
        settings.kafkaconnect.url = "testurl:3000"
        schemaregistry.url = "testurl:8000"

    @pytest.fixture()
    def deployments(self):
        return [
            get_streaming_app_deployment(
                "non-streams-app-deployment", input_topics=None, output_topic=None
            ),
            APP1,
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
        return [
            get_streaming_app_cronjob(
                "non-streams-app-cronjob", input_topics=None, output_topic=None
            ),
            get_streaming_app_cronjob(),
        ]

    @pytest.fixture()
    def fake_linker(self):
        """Creates LinkingService with non-default NodeInfoListItems."""

        class FakeLinker(DefaultLinker):
            def __init__(self):
                super().__init__()
                self.topic_info = [
                    NodeInfoListItem(
                        name="Test Topic Monitoring",
                        value="test",
                        type=NodeInfoType.LINK,
                    ),
                ]

        return FakeLinker()

    @pytest.fixture()
    def streams_explorer(  # noqa: C901
        self, monkeypatch, deployments, cron_jobs, fake_linker
    ):
        monkeypatch.setattr(settings.kafka, "enable", True)

        explorer = StreamsExplorer(
            linking_service=fake_linker, metric_provider=MetricProvider
        )
        extractor_container.extractors = [
            ElasticsearchSink(),
            GenericSink(),
            GenericSource(),
        ]
        monkeypatch.setattr(settings.k8s, "consumer_group_annotation", "consumerGroup")

        async def watch():
            for deployment in deployments + cron_jobs:
                event = {"type": K8sDeploymentEvent.ADDED, "object": deployment}
                explorer.handle_event(event)

        def get_connectors():
            return ["es-sink-connector", "generic-source-connector"]

        def get_connector_info(connector):
            if connector == "es-sink-connector":
                return {
                    "config": {
                        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
                        "test": "test_value",
                        "topics": "output-topic1,output-topic2",
                        "transforms": "changeTopic",
                        "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.RegexRouter",
                        "transforms.changeTopic.regex": ".*",
                        "transforms.changeTopic.replacement": "fake-index",
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

        def get_topic_config(_, topic) -> dict:
            if topic == "input-topic1":
                return {
                    "cleanup.policy": "compact,delete",
                }
            return {}

        def get_topic_partitions(_, topic) -> Optional[dict]:
            if topic == "input-topic1":
                return {i: _ for i in range(5)}
            return None

        def get_all_topic_names(_) -> Set[str]:
            return set()

        monkeypatch.setattr(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
            get_connectors,
        )
        monkeypatch.setattr(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
            get_connector_info,
        )
        monkeypatch.setattr(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.sanitize_connector_config",
            lambda config: config,
        )
        monkeypatch.setattr(
            "streams_explorer.core.services.kafka_admin_client.KafkaAdminClient.get_topic_config",
            get_topic_config,
        )
        monkeypatch.setattr(
            "streams_explorer.core.services.kafka_admin_client.KafkaAdminClient.get_topic_partitions",
            get_topic_partitions,
        )
        monkeypatch.setattr(
            "streams_explorer.core.services.kafka_admin_client.KafkaAdminClient.get_all_topic_names",
            get_all_topic_names,
        )
        monkeypatch.setattr(explorer, "watch", watch)

        return explorer

    @pytest.mark.asyncio
    async def test_update(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        streams_explorer.update_connectors()
        await streams_explorer.update()
        assert len(streams_explorer.applications) == 3
        assert "streaming-app1" in streams_explorer.applications
        assert "streaming-app2" in streams_explorer.applications
        assert "streaming-app3" in streams_explorer.applications
        assert "non-streams-app-deployment" not in streams_explorer.applications
        assert len(streams_explorer.kafka_connectors) == 2

    @pytest.mark.asyncio
    async def test_get_pipeline_names(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        await streams_explorer.update()
        assert streams_explorer.get_pipeline_names() == [
            "pipeline2",
        ]

    @pytest.mark.asyncio
    async def test_get_node_information(
        self, streams_explorer: StreamsExplorer, monkeypatch
    ):
        await streams_explorer.watch()
        streams_explorer.update_connectors()
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
                    name="Partitions",
                    value=5,
                    type=NodeInfoType.BASIC,
                ),
                NodeInfoListItem(
                    name="Cleanup Policy",
                    value="compact,delete",
                    type=NodeInfoType.BASIC,
                ),
                NodeInfoListItem(name="Schema", value={}, type=NodeInfoType.JSON),
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
        result = NodeInformation(
            node_id="es-sink-connector-dead-letter-topic",
            node_type=NodeTypesEnum.ERROR_TOPIC,
            info=[
                NodeInfoListItem(
                    name="Test Topic Monitoring", value="test", type=NodeInfoType.LINK
                ),
                NodeInfoListItem(name="Schema", value={}, type=NodeInfoType.JSON),
            ],
        )
        assert (
            streams_explorer.get_node_information("es-sink-connector-dead-letter-topic")
            == result
        )

        # clear topic_info
        streams_explorer.linking_service.topic_info = []
        # verify caching
        assert (
            streams_explorer.get_node_information("es-sink-connector-dead-letter-topic")
            == result
        )

        streams_explorer.get_node_information.cache_clear()
        assert streams_explorer.get_node_information(
            "es-sink-connector-dead-letter-topic"
        ) == NodeInformation(
            node_id="es-sink-connector-dead-letter-topic",
            node_type=NodeTypesEnum.ERROR_TOPIC,
            info=[
                NodeInfoListItem(name="Schema", value={}, type=NodeInfoType.JSON),
            ],
        )

    @pytest.mark.asyncio
    async def test_cron_job_extractor(self, streams_explorer: StreamsExplorer):
        class MockCronjobExtractor(Extractor):
            def on_cron_job_parsing(self, cron_job: V1beta1CronJob):
                self.cron_job = cron_job
                return K8sAppCronJob(cron_job)

        extractor = MockCronjobExtractor()
        extractor_container.extractors = [extractor]
        await streams_explorer.watch()
        await streams_explorer.update()
        assert extractor.cron_job is not None
        assert extractor.cron_job.metadata is not None
        assert extractor.cron_job.metadata.name == "test-cronjob"
        assert "test-cronjob" in streams_explorer.applications
        assert "non-streams-app-cronjob" not in streams_explorer.applications
        extractor_container.extractors.clear()

    @pytest.mark.asyncio
    async def test_update_sinks_sources(self, streams_explorer: StreamsExplorer):
        class MockAppExtractor(Extractor):
            def _create_source(self, config: K8sConfig) -> Source:
                return Source(
                    node_type="app-source",
                    name=f"{config.id}-source",
                    target=config.id,
                )

            def on_streaming_app_add(self, config: K8sConfig):
                source = self._create_source(config)
                self.sources.append(source)

            def on_streaming_app_delete(self, config: K8sConfig):
                source = self._create_source(config)
                self.sources.remove(source)

        extractor = MockAppExtractor()
        extractor_container.extractors.append(extractor)
        await streams_explorer.watch()
        await streams_explorer.update()
        sources, sinks = extractor_container.get_sources_sinks()
        assert len(sources) == 3
        assert not sinks
        streams_explorer.update_connectors()
        sources, sinks = extractor_container.get_sources_sinks()
        assert len(sources) == 3
        assert len(sinks) == 1
        assert sinks[0].node_type == "elasticsearch-index"

        # updating connectors should only clear sinks & sources added from connectors
        streams_explorer.update_connectors()
        sources, sinks = extractor_container.get_sources_sinks()
        assert len(sources) == 3
        assert len(sinks) == 1

        # deleting app deployment should remove source
        streams_explorer.handle_event(
            {"type": K8sDeploymentEvent.DELETED, "object": APP1}
        )
        sources, sinks = extractor_container.get_sources_sinks()
        assert len(sources) == 2
        assert len(sinks) == 1

    @pytest.mark.asyncio
    async def test_get_link_default(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        streams_explorer.update_connectors()
        await streams_explorer.update()

        # topics
        assert type(streams_explorer.get_link("input-topic1", "grafana")) is str
        assert type(streams_explorer.get_link("input-topic1", "akhq")) is str

        # apps
        assert (
            streams_explorer.get_link("streaming-app2", "grafana")
            == f"{settings.grafana.url}/d/{settings.grafana.dashboards.consumergroups}?var-consumergroups=consumer-group2"
        )

        # connectors
        assert streams_explorer.get_link("es-sink-connector", "grafana") is None
        assert streams_explorer.get_link("es-sink-connector", "akhq") is None
        assert (
            streams_explorer.get_link("generic-source-connector", "grafana")
            == f"{settings.grafana.url}/d/{settings.grafana.dashboards.consumergroups}?var-consumergroups=connect-generic-source"
        )
        assert (
            streams_explorer.get_link("generic-source-connector", "akhq")
            == f"{settings.akhq.url}/ui/{settings.akhq.cluster}/group/connect-generic-source"
        )

        # sinks/sources
        assert (
            streams_explorer.get_link("generic-source-connector", "grafana")
            == f"{settings.grafana.url}/d/{settings.grafana.dashboards.consumergroups}?var-consumergroups=connect-generic-source"
        )

    @pytest.mark.asyncio
    async def test_get_link_kowl(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        streams_explorer.update_connectors()
        await streams_explorer.update()

        # topics
        assert (
            streams_explorer.get_link("input-topic1", "kowl")
            == f"{settings.kowl.url}/topics/input-topic1"
        )

        # apps
        assert (
            streams_explorer.get_link("streaming-app2", "kowl")
            == f"{settings.kowl.url}/groups/consumer-group2"
        )

        # connectors
        assert (
            streams_explorer.get_link("generic-source-connector", "kowl")
            == f"{settings.kowl.url}/groups/connect-generic-source"
        )

    @pytest.mark.asyncio
    async def test_get_link_akhq(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        streams_explorer.update_connectors()
        await streams_explorer.update()

        # topics
        assert (
            streams_explorer.get_link("input-topic1", "akhq")
            == f"{settings.akhq.url}/ui/kubernetes-cluster/topic/input-topic1"
        )

        # apps
        assert (
            streams_explorer.get_link("streaming-app2", "akhq")
            == f"{settings.akhq.url}/ui/kubernetes-cluster/group/consumer-group2"
        )

        # connectors
        assert (
            streams_explorer.get_link("generic-source-connector", "akhq")
            == f"{settings.akhq.url}/ui/kubernetes-cluster/group/connect-generic-source"
        )
        settings.akhq.connect = "kafka-connect"
        assert (
            streams_explorer.get_link("generic-source-connector", "akhq-connect")
            == f"{settings.akhq.url}/ui/{settings.akhq.cluster}/connect/{settings.akhq.connect}/definition/generic-source/tasks"
        )

    @pytest.mark.asyncio
    async def test_get_link_kibanalogs(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        await streams_explorer.update()
        assert (
            streams_explorer.get_link("streaming-app2", "kibanalogs")
            == f"{settings.kibanalogs.url}/app/discover#/?_a=(columns:!(message),query:(language:lucene,query:'kubernetes.labels.app: \"streaming-app2\"'))"
        )

    @pytest.mark.asyncio
    async def test_get_link_loki(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        await streams_explorer.update()
        link = streams_explorer.get_link("streaming-app2", "loki")
        assert link is not None
        assert (
            '/explore?orgId=1&left=["now-1h","now","loki",{"expr":"{app=\\"streaming-app2\\"}"}]'
            in link
        )

    @pytest.mark.asyncio
    async def test_graph_caching(self, streams_explorer: StreamsExplorer):
        await streams_explorer.watch()
        streams_explorer.update_connectors()
        await streams_explorer.update()
        json_graph = streams_explorer.data_flow.json_graph
        assert json_graph
        assert len(json_graph["nodes"]) == 16
        assert len(json_graph["edges"]) == 13

        streams_explorer.data_flow.reset()
        assert not streams_explorer.data_flow.json_graph

    @pytest.mark.asyncio
    async def test_pipeline_graph_caching(
        self, mocker, streams_explorer: StreamsExplorer
    ):
        await streams_explorer.watch()
        streams_explorer.update_connectors()
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
