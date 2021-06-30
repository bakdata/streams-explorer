from pathlib import Path

from streams_explorer.core.config import settings
from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.defaultlinker import DefaultLinker
from streams_explorer.linker import load_linker

fake_linker = """from typing import Optional

from streams_explorer.core.services.linking_services import LinkingService


class FakeLinker(LinkingService):
    def get_redirect_topic(
        self, topic_name: str, link_type: Optional[str]
    ) -> Optional[str]:
        if link_type == "test":
            return f"{topic_name}-link"
        return None
"""


def test_load_default_linker():
    linking_service = load_linker()

    assert isinstance(linking_service(), DefaultLinker)


def test_load_plugin_linker():
    settings.plugins.path = Path.cwd() / "plugins"
    fake_linker_path = settings.plugins.path / "fake_linker.py"
    try:
        with open(fake_linker_path, "w") as f:
            f.write(fake_linker)

        linking_service = load_linker()()

        assert isinstance(linking_service, LinkingService)
        assert not isinstance(linking_service, DefaultLinker)
        assert linking_service.__class__.__name__ == "FakeLinker"
        assert (
            linking_service.get_redirect_topic(topic_name="test", link_type="test")
            == "test-link"
        )
    finally:
        fake_linker_path.unlink()


def test_default_linker_akhq():
    settings.akhq.enable = True
    settings.kowl.enable = False

    linking_service = DefaultLinker()

    # topics
    topic_info = [info_item.value for info_item in linking_service.topic_info]
    assert "akhq" in topic_info
    assert "kowl" not in topic_info

    # apps
    streaming_app_info = [
        info_item.value for info_item in linking_service.streaming_app_info
    ]
    assert "akhq" in streaming_app_info
    assert "kowl" not in streaming_app_info

    # connectors
    connector_info = [info_item.value for info_item in linking_service.connector_info]
    assert "akhq" in connector_info
    assert "kowl" not in connector_info


def test_default_linker_kowl():
    settings.akhq.enable = False
    settings.kowl.enable = True

    linking_service = DefaultLinker()

    # topics
    topic_info = [info_item.value for info_item in linking_service.topic_info]
    assert "kowl" in topic_info
    assert "akhq" not in topic_info

    # apps
    streaming_app_info = [
        info_item.value for info_item in linking_service.streaming_app_info
    ]
    assert "kowl" in streaming_app_info
    assert "akhq" not in streaming_app_info

    # connectors
    connector_info = [info_item.value for info_item in linking_service.connector_info]
    assert "kowl" in connector_info
    assert "akhq" not in connector_info
