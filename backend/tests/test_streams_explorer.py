from typing import List

import pytest
from kubernetes.client import (
    V1beta1CronJob,
    V1beta1CronJobSpec,
    V1beta1JobTemplateSpec,
    V1Container,
    V1EnvVar,
    V1JobSpec,
    V1ObjectMeta,
    V1PodSpec,
    V1PodTemplateSpec,
)

from streams_explorer.core.config import settings
from streams_explorer.core.extractor.default.elasticsearch_sink import ElasticsearchSink
from streams_explorer.core.extractor.default.generic import GenericSink, GenericSource
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.core.k8s_app import K8sAppCronJob
from streams_explorer.core.services.dataflow_graph import NodeTypesEnum
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
        env_prefix = "APP_"
        envs = [
            V1EnvVar(name="ENV_PREFIX", value=env_prefix),
            V1EnvVar(name=env_prefix + "OUTPUT_TOPIC", value="output-topic"),
        ]
        container = V1Container(name="test-container", env=envs)
        pod_spec = V1PodSpec(containers=[container])
        pod_template_spec = V1PodTemplateSpec(spec=pod_spec)
        job_spec = V1JobSpec(
            template=pod_template_spec,
            selector="",
        )
        job_template = V1beta1JobTemplateSpec(spec=job_spec)
        spec = V1beta1CronJobSpec(job_template=job_template, schedule="* * * * *")
        return [V1beta1CronJob(metadata=V1ObjectMeta(name="test-cronjob"), spec=spec)]

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
        extractor_container.extractors = [
            ElasticsearchSink(),
            GenericSink(),
            GenericSource(),
        ]
        monkeypatch.setattr(settings.k8s, "consumer_group_annotation", "consumerGroup")
        mocker.patch.object(
            explorer, attribute="get_deployments", return_value=deployments
        )

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
            "generic-source-connector",
        ]

    def test_get_node_information(self, streams_explorer, monkeypatch):
        streams_explorer.update()
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
                return K8sAppCronJob(cron_job)

        extractor = MockCronjobExtractor()
        extractor_container.extractors = [extractor]
        streams_explorer.update()
        assert extractor.cron_job.metadata.name == "test-cronjob"
        assert "test-cronjob" in streams_explorer.applications
        extractor_container.extractors = []

    def test_get_link(self, streams_explorer):
        streams_explorer.update()
        assert type(streams_explorer.get_link("input-topic1", "grafana")) == str
        assert type(streams_explorer.get_link("input-topic1", "akhq")) == str
        assert "consumergroups=consumer-group2" in streams_explorer.get_link(
            "streaming-app2", "grafana"
        )
        assert type(streams_explorer.get_link("streaming-app2", "kibanalogs")) == str
        assert "consumergroups=connect-generic-source" in streams_explorer.get_link(
            "generic-source-connector", "grafana"
        )
