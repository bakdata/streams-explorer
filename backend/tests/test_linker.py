import os

from server.core.config import settings
from server.core.services.linking_services import LinkingService
from server.defaultlinker import DefaultLinker
from server.linker import load_linker

fake_linker = """
from typing import Optional

from server.core.services.linking_services import LinkingService


class FakeLinker(LinkingService):
    def get_redirect_topic(
        self, topic_name: str, link_type: Optional[str]
    ) -> Optional[str]:
        if link_type == "test":
            return f"{topic_name}-link"
"""


def test_load_default_linker():
    linking_service = load_linker()

    assert isinstance(linking_service(), DefaultLinker)


def test_load_plugin_linker():
    settings.plugins.path = os.path.join(os.getcwd(), "plugins")
    fake_linker_path = os.path.join(settings.plugins.path, "fake_linker.py")
    print(fake_linker_path)
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
        os.remove(fake_linker_path)
