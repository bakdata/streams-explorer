from pathlib import Path

import pytest

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_config_parser import (
    K8sConfigParserArgs,
    K8sConfigParserEnv,
)
from streams_explorer.k8s_config_parser import load_config_parser

config_parser_file = (
    "from streams_explorer.core.k8s_config_parser import K8sConfigParserArgs"
)


class TestK8sConfigParser:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        settings.plugins.path = Path.cwd() / "plugins"
        yield
        settings.plugins.path = "./plugins"

    def test_load_default(self):
        config_parser = load_config_parser()
        assert config_parser is K8sConfigParserEnv

    def test_load_custom(self):
        path = settings.plugins.path / "config_parser.py"
        try:
            with open(path, "w") as f:
                f.write(config_parser_file)

            config_parser = load_config_parser()
            assert config_parser is K8sConfigParserArgs
        finally:
            path.unlink()
