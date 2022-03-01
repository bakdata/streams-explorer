from enum import Enum
from typing import List, Optional

import pydantic
from cfgv import ValidationError
from loguru import logger
from pydantic import BaseConfig, BaseModel, Extra

from streams_explorer.core.extractor.default.transformer import TRANSFORMER


class KafkaConnectorTypesEnum(str, Enum):
    SINK = "sink"
    SOURCE = "source"


class KafkaConnectorConfig(BaseModel):
    topics: Optional[str]
    transforms: Optional[str]

    class Config(BaseConfig):
        extra = Extra.allow

    def get_transforms(self) -> List[str]:
        if self.transforms is not None:
            return self.transforms.split(",")
        return []


class KafkaConnector(BaseModel):
    name: str
    type: KafkaConnectorTypesEnum
    config: KafkaConnectorConfig
    error_topic: Optional[str] = None
    topics: List[
        str
    ] = []  # Deprecated please override get_topics for your kafka connector.

    def get_topics(self) -> List[str]:
        """
        Override in your kafka connector. Use the config to retrieve and parse the topics.
        This implementation only ensures the support of (older) plugins that use the deprecated topics field.
        """
        return self.topics

    def get_routes(self) -> List[str]:
        """
        Applies the single message transformers to get target routes (e.g. for the ElasticSearchSinkConnector)
        """
        routes = self.get_topics()
        transforms = self.config.get_transforms()
        for transformer_name in transforms:
            routes = self.apply_transformer(routes, transformer_name)
        return list(set(routes))

    def apply_transformer(self, indices, transformer_name) -> List[str]:
        transformer_prefix = KafkaConnector.get_transformer_prefix(transformer_name)
        # transformer config without transformer_prefix
        transformer_config = {
            config_name.replace(transformer_prefix, ""): config_value
            for config_name, config_value in self.config.dict().items()
            if KafkaConnector.is_transformer_config(config_name, transformer_prefix)
        }
        transformer_config["topics"] = indices
        try:
            transformer = pydantic.parse_obj_as(TRANSFORMER, transformer_config)
            return transformer.get_routes()
        except ValidationError as e:
            logger.exception(
                f"Failed to apply transformer {transformer_name} on {self.name}", e
            )
            return []

    @staticmethod
    def get_transformer_prefix(transformer_name: str) -> str:
        return f"transforms.{transformer_name}."

    @staticmethod
    def is_transformer_config(key: str, transformer_prefix: str) -> bool:
        return key.startswith(transformer_prefix)
