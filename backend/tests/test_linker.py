from pathlib import Path

import pytest
from dynaconf.validator import ValidationError

from streams_explorer.core.config import settings
from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.defaultlinker import DefaultLinker
from streams_explorer.linker import load_linker
from streams_explorer.models.node_information import NodeInfoListItem

fake_linker = """from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.services.linking_services import LinkingService


class FakeLinker(LinkingService):
    def get_redirect_connector(self, config: dict, link_type: str) -> str | None:
        pass

    def get_redirect_topic(
        self, topic_name: str, link_type: str
    ) -> str | None:
        match link_type:
            case "test":
                return f"{topic_name}-link"

    def get_redirect_streaming_app(
        self, k8s_app: K8sApp, link_type: str
    ) -> str | None:
        pass

    def get_sink_source_redirects(
        self, node_type: str, sink_source_name: str
    ) -> str | None:
        pass
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
        settings.plugins.path = "./plugins"


def get_info_providers(info_list: list[NodeInfoListItem]):
    return [info_item.value for info_item in info_list]


def test_default_linker_akhq():
    settings.akhq.enable = True
    settings.redpanda_console.enable = False
    settings.validators.validate()

    linking_service = DefaultLinker()

    topic_info = get_info_providers(linking_service.topic_info)
    assert "akhq" in topic_info
    assert "redpanda_console" not in topic_info

    streaming_app_info = get_info_providers(linking_service.streaming_app_info)
    assert "akhq" in streaming_app_info
    assert "redpanda_console" not in streaming_app_info

    connector_info = get_info_providers(linking_service.connector_info)
    assert "akhq" in connector_info
    assert "akhq-connect" not in connector_info
    assert "redpanda_console" not in connector_info

    settings.akhq.connect = "kafka-connect"
    linking_service = DefaultLinker()
    assert "akhq-connect" in get_info_providers(linking_service.connector_info)


def test_default_linker_redpanda_console():
    settings.akhq.enable = False
    settings.redpanda_console.enable = True
    settings.validators.validate()

    linking_service = DefaultLinker()

    topic_info = get_info_providers(linking_service.topic_info)
    assert "redpanda_console" in topic_info
    assert "akhq" not in topic_info

    streaming_app_info = get_info_providers(linking_service.streaming_app_info)
    assert "redpanda_console" in streaming_app_info
    assert "akhq" not in streaming_app_info

    connector_info = get_info_providers(linking_service.connector_info)
    assert "redpanda_console" in connector_info
    assert "akhq" not in connector_info
    assert "akhq-connect" not in connector_info


def test_default_linker_akhq_redpanda_console():
    settings.akhq.enable = True
    settings.redpanda_console.enable = True
    with pytest.raises(ValidationError):
        settings.validators.validate()

    settings.akhq.enable = False
    settings.redpanda_console.enable = False
    settings.validators.validate()


def test_default_linker_kibanalogs():
    settings.kibanalogs.enable = True
    settings.loki.enable = False
    settings.validators.validate()

    linking_service = DefaultLinker()

    streaming_app_info = get_info_providers(linking_service.streaming_app_info)
    assert "kibanalogs" in streaming_app_info
    assert "loki" not in streaming_app_info


def test_default_linker_loki():
    settings.kibanalogs.enable = False
    settings.loki.enable = True
    settings.validators.validate()

    linking_service = DefaultLinker()

    streaming_app_info = get_info_providers(linking_service.streaming_app_info)
    assert "loki" in streaming_app_info
    assert "kibanalogs" not in streaming_app_info


def test_default_linker_kibanalogs_loki():
    settings.kibanalogs.enable = True
    settings.loki.enable = True
    with pytest.raises(ValidationError):
        settings.validators.validate()

    settings.kibanalogs.enable = False
    settings.loki.enable = False
    settings.validators.validate()


def test_default_linker_grafana_enabled():
    settings.grafana.enable = True
    settings.validators.validate()

    linking_service = DefaultLinker()

    assert "grafana" in get_info_providers(linking_service.topic_info)
    assert "grafana" in get_info_providers(linking_service.streaming_app_info)
    assert "grafana" in get_info_providers(linking_service.connector_info)


def test_default_linker_grafana_disabled():
    del settings.grafana.enable
    settings.validators.validate()

    linking_service = DefaultLinker()

    assert "grafana" not in get_info_providers(linking_service.topic_info)
    assert "grafana" not in get_info_providers(linking_service.streaming_app_info)
    assert "grafana" not in get_info_providers(linking_service.connector_info)
