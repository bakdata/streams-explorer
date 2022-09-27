from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from streams_explorer.core.config import settings
from streams_explorer.core.extractor.extractor import (
    ProducerAppExtractor,
    StreamsAppExtractor,
)
from streams_explorer.core.services.kafkaconnect import KafkaConnect
from streams_explorer.extractors import extractor_container, load_extractors
from streams_explorer.models.kafka_connector import KafkaConnectorTypesEnum

extractor_file_1 = """from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink


class TestSinkOne(Extractor):
    def on_connector_info_parsing(
        self, config: dict, connector_name: str
    ) -> KafkaConnector | None:
        self.sinks.append(
            Sink(
                name="test",
                node_type="elasticsearch-index",
                source=connector_name,
            )
        )
"""

extractor_file_2 = """from streams_explorer.core.extractor.extractor import ConnectorExtractor
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.sink import Sink


class TestSinkTwo(ConnectorExtractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        self.sinks.append(
            Sink(
                name="test",
                node_type="elasticsearch-index",
                source=connector_name,
            )
        )
"""

extractor_file_3 = """from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from kubernetes_asyncio.client import V1beta1CronJob
from streams_explorer.models.k8s import K8sConfig
from streams_explorer.core.extractor.extractor import (
    CronJobExtractor,
    StreamsAppExtractor,
)

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sAppCronJob

class TestMultipleExtractor(StreamsAppExtractor, CronJobExtractor):
    def on_streaming_app_add(self, config: K8sConfig) -> None:
        pass

    def on_streaming_app_delete(self, config: K8sConfig) -> None:
        pass

    def on_cron_job_parsing(self, cron_job: V1beta1CronJob) -> K8sAppCronJob | None:
        pass
"""

EMPTY_CONNECTOR_INFO = {"config": {}, "type": ""}


class TestExtractors:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        # setup
        settings.kafkaconnect.url = "testurl:3000"
        yield  # testing
        # teardown
        settings.plugins.path = "./plugins"
        extractor_container.extractors.clear()

    def test_load_extractors(self):
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
                extractor.__class__.__name__
                for extractor in extractor_container.extractors
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

    def test_load_extractor_multiple_inheritance(self):
        settings.plugins.extractors.default = False
        settings.plugins.path = Path.cwd() / "plugins"
        extractor_3_path = settings.plugins.path / "fake_extractor_3.py"
        try:
            with open(extractor_3_path, "w") as f:
                f.write(extractor_file_3)

            load_extractors()
            assert len(extractor_container.extractors) == 3

            extractor = extractor_container.extractors[0]
            assert extractor.__class__.__name__ == "TestMultipleExtractor"
            assert isinstance(extractor, StreamsAppExtractor)
            assert isinstance(extractor, ProducerAppExtractor)
        finally:
            extractor_3_path.unlink()

    def test_load_extractors_without_defaults(self):
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

    def test_generic_extractors_fallback(self, mocker: MockerFixture):
        settings.plugins.extractors.default = True
        load_extractors()

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
                        "topics": "my-topic-1,my-topic-2",
                        "errors.deadletterqueue.topic.name": "dead-letter-topic",
                    },
                }
            if connector_name == "custom-source":
                return {
                    "type": "source",
                    "config": {"connector.class": "CustomSourceConnector"},
                }
            return {}

        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
            get_connector_info,
        )

        connectors = KafkaConnect.connectors()
        assert len(connectors) == 2
        assert connectors[0].type == KafkaConnectorTypesEnum.SINK
        assert connectors[0].get_topics() == ["my-topic-1", "my-topic-2"]
        assert connectors[0].get_error_topic() == "dead-letter-topic"
        assert connectors[1].type == KafkaConnectorTypesEnum.SOURCE
        assert connectors[1].get_topics() == []
        assert connectors[1].get_error_topic() is None

    def test_extractors_topics_none(self, mocker: MockerFixture):
        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
            lambda _: EMPTY_CONNECTOR_INFO,
        )
        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
            lambda: ["connector"],
        )

        on_connector_info_parsing = mocker.spy(
            extractor_container, "on_connector_info_parsing"
        )
        KafkaConnect.connectors()
        assert on_connector_info_parsing.call_count == 1

    def test_elasticsearch_sink(self):
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
                    "topics": "my-topic-1,my-topic-2",
                    "transforms": "changeTopic",
                    "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.RegexRouter",
                    "transforms.changeTopic.replacement": "es-test-index",
                    "errors.deadletterqueue.topic.name": "dead-letter-topic",
                }
            },
            "elasticsearch-sink-connector",
        )
        assert len(extractor.sinks) == 1
        assert extractor.sinks[0].name == "es-test-index"
        assert connector is not None
        assert connector.get_topics() == ["my-topic-1", "my-topic-2"]
        assert connector.get_error_topic() == "dead-letter-topic"

    def test_s3_sink(self):
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

    def test_jdbc_sink(self):
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
