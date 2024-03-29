import pytest
from pytest import MonkeyPatch

from streams_explorer.core.config import settings, sort_displayed_information
from streams_explorer.core.k8s_app import K8sAppDeployment
from streams_explorer.core.node_info_extractor import (
    get_displayed_information_connector,
    get_displayed_information_deployment,
    get_displayed_information_topic,
)
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorConfig,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.node_information import NodeInfoListItem, NodeInfoType
from tests.utils import get_streaming_app_deployment


class TestNodeInfoExtractor:
    @pytest.fixture(autouse=True)
    def kafka_connect(self):
        settings.kafkaconnect.url = "testurl:3000"
        settings.kafkaconnect.displayed_information = []

    def test_sort_displayed_information_alphabetic(self):
        assert sort_displayed_information(
            [
                {"name": "Test1", "key": "test"},
                {"name": "bar", "key": "foo.bar"},
                {"name": "testlist", "key": "foo.test"},
            ]
        ) == [
            {"name": "bar", "key": "foo.bar"},
            {"name": "Test1", "key": "test"},
            {"name": "testlist", "key": "foo.test"},
        ]

    def test_get_displayed_information_connector(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(
            settings.kafkaconnect,
            "displayed_information",
            [
                {"name": "Test1", "key": "test"},
                {"name": "bar", "key": "foo.bar"},
                {"name": "testlist", "key": "foo.test"},
            ],
        )

        connector = KafkaConnector(
            name="test-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "test": "testValue",
                    "foo": {"bar": {"testDict": "test"}, "test": ["test", "test"]},
                },
                topics="topic1"
            ),
        )

        output = get_displayed_information_connector(connector.config.dict())
        assert (
            NodeInfoListItem(name="Test1", value="testValue", type=NodeInfoType.BASIC)
            in output
        )
        assert (
            NodeInfoListItem(
                name="bar",
                value=connector.config.dict()["foo"]["bar"],
                type=NodeInfoType.JSON,
            )
            in output
        )
        assert (
            NodeInfoListItem(
                name="testlist",
                value=str(connector.config.dict()["foo"]["test"]),
                type=NodeInfoType.BASIC,
            )
            in output
        )

    def test_get_displayed_information_deyployment(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(
            settings.k8s,
            "displayed_information",
            [
                {"name": "Labels", "key": "metadata.labels"},
                {"name": "Pipeline", "key": "metadata.labels.pipeline"},
            ],
        )

        k8s_app = get_streaming_app_deployment(
            "streaming-app1",
            "input-topic1",
            "output-topic1",
            "error-topic1",
            pipeline="pipeline1",
        )
        output = get_displayed_information_deployment(K8sAppDeployment(k8s_app))

        assert len(output) == 2
        value = output[0].value
        assert "pipeline" in value
        assert output[1] == NodeInfoListItem(
            name="Pipeline", value="pipeline1", type=NodeInfoType.BASIC
        )

    def test_get_displayed_information_topic(self, monkeypatch: MonkeyPatch):
        assert get_displayed_information_topic({}) == []

        kafka_topic_config = {
            "cleanup.policy": "delete",
            "retention.ms": "-1",
        }
        output = get_displayed_information_topic(kafka_topic_config)
        assert len(output) == 1
        assert output == [
            NodeInfoListItem(
                name="Cleanup Policy", value="delete", type=NodeInfoType.BASIC
            ),
        ]

        # Change displayed information
        monkeypatch.setattr(
            settings.kafka,
            "displayed_information",
            [
                {"name": "Cleanup Policy", "key": "cleanup.policy"},
                {"name": "Retention", "key": "retention.ms"},
            ],
        )
        output = get_displayed_information_topic(kafka_topic_config)
        assert len(output) == 2
        assert output == [
            NodeInfoListItem(
                name="Cleanup Policy", value="delete", type=NodeInfoType.BASIC
            ),
            NodeInfoListItem(name="Retention", value="-1", type=NodeInfoType.BASIC),
        ]
