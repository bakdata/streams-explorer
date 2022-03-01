from enum import Enum
from typing import List, Optional, Union

import pydantic
from loguru import logger
from pydantic import BaseConfig, BaseModel, Extra, Field, ValidationError

from streams_explorer.core.extractor.default.transformer import (
    GenericTransformerConfig,
    RegexRouterTransformerConfig,
    TimestampRouterTransformerConfig,
)


class KafkaConnectorTypesEnum(str, Enum):
    SINK = "sink"
    SOURCE = "source"


class KafkaConnectorConfig(BaseModel):
    topics: Optional[str]
    transforms: Optional[str]
    error_topic: Optional[str] = Field(
        default=None, alias="errors.deadletterqueue.topic.name"
    )

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
    error_topic: Optional[str]
    topics: Optional[
        List[str]
    ]  # Deprecated please override get_topics for your kafka connector.

    # Do not change order here. The fallback GenericTransformerConfig should always be the last element
    _transformers = Union[
        RegexRouterTransformerConfig,
        TimestampRouterTransformerConfig,
        GenericTransformerConfig,
    ]

    def get_topics(self) -> List[str]:
        """
        Override in your kafka connector. Use the config to retrieve and parse the topics.
        This implementation only ensures the support of (older) plugins that use the deprecated topics field.
        """
        if self.topics is None:
            return KafkaConnector.split_topics(self.config.topics)
        return self.topics

    def get_error_topic(self):
        if self.error_topic is not None:
            return self.error_topic
        return self.config.error_topic

    @staticmethod
    def split_topics(topics: Optional[str]) -> List[str]:
        if topics:
            return topics.replace(" ", "").split(",")
        return []

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
            transformer = pydantic.parse_obj_as(self._transformers, transformer_config)
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
