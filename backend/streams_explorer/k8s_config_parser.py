from typing import Type

from loguru import logger

from streams_explorer.core.k8s_config_parser import (
    K8sConfigParser,
    StreamsBootstrapEnvParser,
)
from streams_explorer.plugins import load_plugin


def load_config_parser() -> Type[K8sConfigParser]:
    parser = load_plugin(K8sConfigParser)
    if (
        not parser
        or not isinstance(parser, type)
        or not issubclass(parser, K8sConfigParser)
    ):
        logger.info("Using default K8sConfigParser")
        return StreamsBootstrapEnvParser
    logger.info(f"Using custom K8sConfigParser: {parser.__name__}")
    return parser
