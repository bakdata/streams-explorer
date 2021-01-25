from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.node_info_extractor import (
    get_displayed_information_connector,
    get_displayed_information_deployment,
)
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.node_information import NodeInfoListItem, NodeInfoType
from tests.utils import get_streaming_app_deployment


class TestNodeInfoExtractor:
    def test_get_displayed_information_connector(self, monkeypatch):
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
            topics=["topic1"],
            config={
                "test": "testValue",
                "foo": {"bar": {"testDict": "test"}, "test": ["test", "test"]},
            },
        )

        output = get_displayed_information_connector(connector.config)
        assert (
            NodeInfoListItem(name="Test1", value="testValue", type=NodeInfoType.BASIC)
            in output
        )
        assert (
            NodeInfoListItem(
                name="bar",
                value=connector.config.get("foo").get("bar"),
                type=NodeInfoType.JSON,
            )
            in output
        )
        assert (
            NodeInfoListItem(
                name="testlist",
                value=str(connector.config.get("foo").get("test")),
                type=NodeInfoType.BASIC,
            )
            in output
        )

    def test_get_displayed_information_deyployment(self, monkeypatch):
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
        output = get_displayed_information_deployment(K8sApp(k8s_app))

        assert len(output) == 2
        value = output[0].value
        assert "pipeline" in value
        assert output[1] == NodeInfoListItem(
            name="Pipeline", value="pipeline1", type=NodeInfoType.BASIC
        )
