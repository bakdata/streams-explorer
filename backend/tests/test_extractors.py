from pathlib import Path

from streams_explorer.core.config import settings
from streams_explorer.core.services.kafkaconnect import KafkaConnect
from streams_explorer.extractors import extractor_container, load_extractors
from streams_explorer.models.kafka_connector import KafkaConnectorTypesEnum

extractor_file_1 = """from typing import List, Optional

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink


class TestSinkOne(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_info_parsing(
        self, config: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        self.sinks.append(
            Sink(
                name="test",
                node_type="elasticsearch-index",
                source=connector_name,
            )
        )
        return None
"""

extractor_file_2 = """from typing import List, Optional

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink


class TestSinkTwo(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        self.sinks.append(
            Sink(
                name="test",
                node_type="elasticsearch-index",
                source=connector_name,
            )
        )
        return None
"""

EMPTY_CONNECTOR_INFO = {"config": {}, "type": ""}


def test_load_extractors():
    settings.plugins.extractors.default = True
    settings.plugins.path = Path.cwd() / "plugins"
    assert len(extractor_container.extractors) == 3
    extractor_1_path = settings.plugins.path / "fake_extractor_1.py"
    extractor_2_path = settings.plugins.path / "fake_extractor_2.py"
    try:
        with open(extractor_1_path, "w") as f:
            f.write(extractor_file_1)

        with open(extractor_2_path, "w") as f:
            f.write(extractor_file_2)

        load_extractors()

        assert len(extractor_container.extractors) == 7

        extractor_classes = [
            extractor.__class__.__name__ for extractor in extractor_container.extractors
        ]
        assert "TestSinkOne" in extractor_classes
        assert "TestSinkTwo" in extractor_classes
        assert "ElasticsearchSink" in extractor_classes
        assert "S3Sink" in extractor_classes
        assert "JdbcSink" in extractor_classes
        # Verify Generic extractors are last in list as fallback
        fallback_extractor_classes = extractor_classes[-2:]
        assert "GenericSink" in fallback_extractor_classes
        assert "GenericSource" in fallback_extractor_classes
    finally:
        extractor_1_path.unlink()
        extractor_2_path.unlink()


def test_load_extractors_without_defaults():
    settings.plugins.extractors.default = False
    settings.plugins.path = Path.cwd() / "plugins"
    extractor_container.extractors.clear()
    load_extractors()

    assert len(extractor_container.extractors) == 2

    extractor_classes = [
        extractor.__class__.__name__ for extractor in extractor_container.extractors
    ]
    assert "GenericSink" in extractor_classes
    assert "GenericSource" in extractor_classes


def test_generic_extractors_fallback(mocker):
    settings.plugins.extractors.default = True

    mocker.patch(
        "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
        lambda: ["custom-sink", "custom-source"],
    )

    def get_connector_info(connector_name: str) -> dict:
        if connector_name == "custom-sink":
            return {
                "type": "sink",
                "config": {
                    "connector.class": "CustomSinkConnector",
                    "topics": "my-topic-1, my-topic-2",
                    "errors.deadletterqueue.topic.name": "dead-letter-topic",
                },
            }
        if connector_name == "custom-source":
            return {
                "type": "source",
                "config": {
                    "connector.class": "CustomSourceConnector",
                },
            }
        return {}

    mocker.patch(
        "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
        get_connector_info,
    )

    connectors = KafkaConnect.connectors()
    assert len(connectors) == 2
    assert connectors[0].type == KafkaConnectorTypesEnum.SINK
    assert connectors[0].topics == ["my-topic-1", "my-topic-2"]
    assert connectors[0].error_topic == "dead-letter-topic"
    assert connectors[1].type == KafkaConnectorTypesEnum.SOURCE
    assert connectors[1].topics == []
    assert connectors[1].error_topic is None


def test_extractors_topics_none(mocker):
    mocker.patch(
        "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
        lambda connector: EMPTY_CONNECTOR_INFO,
    )
    mocker.patch(
        "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
        lambda: ["connector"],
    )

    on_connector_info_parsing = mocker.spy(
        extractor_container, "on_connector_info_parsing"
    )
    KafkaConnect.connectors()
    on_connector_info_parsing.assert_called_once()


def test_elasticsearch_sink():
    from streams_explorer.core.extractor.default.elasticsearch_sink import (
        ElasticsearchSink,
    )

    extractor = ElasticsearchSink()
    extractor.on_connector_info_parsing(EMPTY_CONNECTOR_INFO, "")
    assert len(extractor.sinks) == 0
    extractor.on_connector_info_parsing(
        {
            "config": {
                "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector"
            }
        },
        "elasticsearch-test-sink",
    )
    assert len(extractor.sinks) == 0
    connector = extractor.on_connector_info_parsing(
        {
            "config": {
                "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
                "transforms.changeTopic.replacement": "es-test-index",
                "topics": "my-topic-1, my-topic-2",
                "errors.deadletterqueue.topic.name": "dead-letter-topic",
            }
        },
        "elasticsearch-sink-connector",
    )
    assert len(extractor.sinks) == 1
    assert extractor.sinks[0].name == "es-test-index"
    assert connector.topics == ["my-topic-1", "my-topic-2"]
    assert connector.error_topic == "dead-letter-topic"


def test_s3_sink():
    from streams_explorer.core.extractor.default.s3_sink import S3Sink

    extractor = S3Sink()
    extractor.on_connector_info_parsing(EMPTY_CONNECTOR_INFO, "")
    assert len(extractor.sinks) == 0
    extractor.on_connector_info_parsing(
        {
            "config": {
                "connector.class": "io.confluent.connect.s3.S3SinkConnector",
                "s3.bucket.name": "s3-test-bucket",
            }
        },
        "s3-sink-connector",
    )
    assert len(extractor.sinks) == 1
    assert extractor.sinks[0].name == "s3-test-bucket"


def test_jdbc_sink():
    from streams_explorer.core.extractor.default.jdbc_sink import JdbcSink

    extractor = JdbcSink()
    extractor.on_connector_info_parsing(EMPTY_CONNECTOR_INFO, "")
    assert len(extractor.sinks) == 0
    extractor.on_connector_info_parsing(
        {
            "config": {
                "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
                "table.name.format": "jdbc-table",
            }
        },
        "jdbc-sink-connector",
    )
    assert len(extractor.sinks) == 1
    assert extractor.sinks[0].name == "jdbc-table"
