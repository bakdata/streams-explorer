import os

from streams_explorer.core.config import settings
from streams_explorer.core.extractor.extractor_container import ExtractorContainer
from streams_explorer.extractors import extractor_container, load_extractors

extractor_file_1 = """from typing import List
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class TestSinkOne(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(self, config, connector_name):
        self.sinks.append(
            Sink(
                name="test",
                node_type="elasticsearch-index",
                source=connector_name,
            )
        )
            """

extractor_file_2 = """from typing import List
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class TestSinkTwo(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(self, config, connector_name):
        self.sinks.append(
            Sink(
                name="test",
                node_type="elasticsearch-index",
                source=connector_name,
            )
        )
            """


def test_load_extractors():
    settings.plugins.extractors.default = True
    settings.plugins.path = os.getcwd()
    assert len(extractor_container.extractors) == 3
    file_path_1 = os.path.join(settings.plugins.path, "test_extractor1.py")
    file_path_2 = os.path.join(settings.plugins.path, "test_extractor2.py")
    try:
        with open(file_path_1, "w") as f:
            f.write(extractor_file_1)

        with open(file_path_2, "w") as f:
            f.write(extractor_file_2)

        load_extractors()

        assert len(extractor_container.extractors) == 5

        extractor_classes = [
            extractor.__class__.__name__ for extractor in extractor_container.extractors
        ]
        assert "TestSinkOne" in extractor_classes
        assert "TestSinkTwo" in extractor_classes
        assert "ElasticsearchSink" in extractor_classes
        assert "S3Sink" in extractor_classes
        assert "JdbcSink" in extractor_classes
    finally:
        os.remove(file_path_1)
        os.remove(file_path_2)


def test_load_extractors_without_defaults():
    settings.plugins.extractors.default = False
    settings.plugins.path = os.getcwd()
    extractor_container = ExtractorContainer()  # noqa: F811
    load_extractors()

    assert len(extractor_container.extractors) == 0


def test_elasticsearch_sink():
    from streams_explorer.core.extractor.default.elasticsearch_sink import (
        ElasticsearchSink,
    )

    extractor = ElasticsearchSink()
    extractor.on_connector_config_parsing({}, "")
    assert len(extractor.sinks) == 0
    extractor.on_connector_config_parsing(
        {
            "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector"
        },
        "elasticsearch-test-sink",
    )
    assert len(extractor.sinks) == 0
    extractor.on_connector_config_parsing(
        {
            "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
            "transforms.changeTopic.replacement": "es-test-index",
        },
        "elasticsearch-sink-connector",
    )
    assert len(extractor.sinks) == 1
    assert extractor.sinks[0].name == "es-test-index"


def test_s3_sink():
    from streams_explorer.core.extractor.default.s3_sink import S3Sink

    extractor = S3Sink()
    extractor.on_connector_config_parsing({}, "")
    assert len(extractor.sinks) == 0
    extractor.on_connector_config_parsing(
        {
            "connector.class": "io.confluent.connect.s3.S3SinkConnector",
            "s3.bucket.name": "s3-test-bucket",
        },
        "s3-sink-connector",
    )
    assert len(extractor.sinks) == 1
    assert extractor.sinks[0].name == "s3-test-bucket"


def test_jdbc_sink():
    from streams_explorer.core.extractor.default.jdbc_sink import JdbcSink

    extractor = JdbcSink()
    extractor.on_connector_config_parsing({}, "")
    assert len(extractor.sinks) == 0
    extractor.on_connector_config_parsing(
        {
            "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
            "name": "jdbc-test-sink",
        },
        "jdbc-sink-connector",
    )
    assert len(extractor.sinks) == 1
    assert extractor.sinks[0].name == "jdbc-test-sink"
