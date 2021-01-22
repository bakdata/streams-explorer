from typing import List

import pytest
from kubernetes.client import V1beta1CronJob, V1ObjectMeta

from streams_explorer.core.config import settings
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.core.services.dataflow_graph import NodeTypesEnum
from streams_explorer.defaultlinker import DefaultLinker
from streams_explorer.extractors import extractor_container
from streams_explorer.models.node_information import (
    NodeInfoListItem,
    NodeInformation,
    NodeInfoType,
)
from streams_explorer.models.source import Source
from streams_explorer.streams_explorer import StreamsExplorer
from tests.utils import get_streaming_app_deployment


class TestStreamsExplorer:
    @staticmethod
    def get_topic_value_schema(topic, version):
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
                "streaming-app2", "input-topic2", "output-topic2", "error-topic2"
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
        return [V1beta1CronJob(metadata=V1ObjectMeta(name="test"))]

    @pytest.fixture()
    def fake_linker(self, mocker):
        """Creates LinkingService without default NodeInfoListItems."""

        def fake_linker_init(self):
            pass

        mocker.patch(
            "streams_explorer.defaultlinker.DefaultLinker.__init__",
            fake_linker_init,
        )
        return DefaultLinker()

    @pytest.fixture()
    def streams_explorer(
        self, mocker, deployments, cron_jobs, monkeypatch, fake_linker
    ):
        explorer = StreamsExplorer(linking_service=fake_linker)
        extractor_container.extractors = []
        mocker.patch.object(
            explorer, attribute="get_deployments", return_value=deployments
        )

        mocker.patch.object(explorer, attribute="get_cron_jobs", return_value=cron_jobs)

        def get_connectors():
            return ["connector1", "connector2"]

        def get_connector_info(connector):
            if connector == "connector1":
                return ["output-topic1", "output-topic2"], {"test": "test_value"}
            return ["output-topic3"], {"test": "test_value"}

        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
            get_connectors,
        )
        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
            get_connector_info,
        )

        mocker.patch(
            "streams_explorer.core.services.schemaregistry.SchemaRegistry.get_topic_value_schema_versions",
            lambda topic: [1, 2],
        )
        mocker.patch(
            "streams_explorer.core.services.schemaregistry.SchemaRegistry.get_topic_value_schema",
            self.get_topic_value_schema,
        )

        return explorer

    def test_update(self, streams_explorer):
        streams_explorer.update()
        assert len(streams_explorer.applications) == 3
        assert len(streams_explorer.kafka_connectors) == 2

    def test_get_pipeline_names(self, streams_explorer):
        streams_explorer.update()
        assert streams_explorer.get_pipeline_names() == [
            "streaming-app1",
            "pipeline2",
        ]

    def test_get_node_information(self, streams_explorer, deployments, monkeypatch):
        streams_explorer.update()
        monkeypatch.setattr(
            settings.kafkaconnect,
            "displayed_information",
            [{"name": "test", "key": "test"}],
        )
        monkeypatch.setattr(
            settings.k8s,
            "displayed_information",
            [{"name": "Source Type", "key": "metadata.labels.source_type"}],
        )

        assert streams_explorer.get_node_information("connector1") == NodeInformation(
            node_id="connector1",
            node_type=NodeTypesEnum.CONNECTOR,
            info=[
                NodeInfoListItem(
                    name="test", value="test_value", type=NodeInfoType.BASIC
                )
            ],
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
                    name="Schema",
                    value=self.get_topic_value_schema("", 2),
                    type=NodeInfoType.JSON,
                )
            ],
        )

    def test_cron_job_extractor(self, streams_explorer):
        class MockCronjobExtractor(Extractor):
            def __init__(self):
                self.sources: List[Source] = []
                self.cron_job = None

            def on_cron_job_parsing(self, cron_job: V1beta1CronJob):
                self.cron_job = cron_job

        extractor = MockCronjobExtractor()
        extractor_container.extractors = [extractor]
        streams_explorer.update()
        assert extractor.cron_job.metadata.name == "test"
        extractor_container.extractors = []

    def test_get_link(self, streams_explorer):
        streams_explorer.update()
        assert type(streams_explorer.get_link("input-topic1", "grafana")) == str
        assert type(streams_explorer.get_link("input-topic1", "akhq")) == str
        assert type(streams_explorer.get_link("streaming-app2", None)) == str
