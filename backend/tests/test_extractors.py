from pathlib import Path

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
    settings.plugins.path = Path.cwd() / "plugins"
    assert len(extractor_container.extractors) == 1
    extractor_1_path = settings.plugins.path / "fake_extractor_1.py"
    extractor_2_path = settings.plugins.path / "fake_extractor_2.py"
    try:
        with open(extractor_1_path, "w") as f:
            f.write(extractor_file_1)

        with open(extractor_2_path, "w") as f:
            f.write(extractor_file_2)

        load_extractors()

        assert len(extractor_container.extractors) == 3

        extractor_classes = [
            extractor.__class__.__name__ for extractor in extractor_container.extractors
        ]
        assert "TestSinkOne" in extractor_classes
        assert "TestSinkTwo" in extractor_classes
        assert "ElasticsearchSink" in extractor_classes
    finally:
        extractor_1_path.unlink()
        extractor_2_path.unlink()


def test_load_extractors_without_defaults():
    settings.plugins.extractors.default = False
    settings.plugins.path = Path.cwd() / "plugins"
    extractor_container = ExtractorContainer()  # noqa: F811
    load_extractors()

    assert len(extractor_container.extractors) == 0
