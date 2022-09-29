from loguru import logger

from streams_explorer.core.k8s_config_parser import (
    K8sConfigParser,
    StreamsBootstrapEnvParser,
)
from streams_explorer.plugins import load_plugin


def load_config_parser() -> type[K8sConfigParser]:
    parser = load_plugin(K8sConfigParser)  # type: ignore[misc]
    if not parser:
        logger.info("Using default K8sConfigParser")
        return StreamsBootstrapEnvParser
    logger.info(f"Using custom K8sConfigParser: {parser.__name__}")
    return parser
