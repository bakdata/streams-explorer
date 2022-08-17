from enum import Enum
from typing import Union

import pydantic
from loguru import logger
from pydantic import BaseConfig, BaseModel, Extra, Field, ValidationError

from streams_explorer.core.extractor.default.transformer import (
    GenericTransformerConfig,
    RegexRouterTransformerConfig,
    RouterTransformerConfig,
    TimestampRouterTransformerConfig,
)


class KafkaConnectorTypesEnum(str, Enum):
    SINK = "sink"
    SOURCE = "source"


class KafkaConnectorConfig(BaseModel):
    topics: str | None = Field(default=None)
    transforms: str | None = Field(default=None)
    error_topic: str | None = Field(
        default=None, alias="errors.deadletterqueue.topic.name"
    )

    class Config(BaseConfig):
        extra = Extra.allow

    def get_transforms(self) -> list[str]:
        if self.transforms is not None:
            return self.transforms.split(",")
        return []


class KafkaConnector(BaseModel):
    name: str
    type: KafkaConnectorTypesEnum
    config: KafkaConnectorConfig
    error_topic: str | None = Field(default=None)
    topics: list[str] | None = Field(
        default=None
    )  # Deprecated please override get_topics for your kafka connector.

    # Do not change order here. The fallback GenericTransformerConfig should always be the last element
    _transformers = Union[
        RegexRouterTransformerConfig,
        TimestampRouterTransformerConfig,
        GenericTransformerConfig,
    ]

    def get_topics(self) -> list[str]:
        """
        Override in your kafka connector. Use the config to retrieve and parse the topics.
        This implementation only ensures the support of (older) plugins that use the deprecated topics field.
        """
        if self.topics is None:
            return KafkaConnector.split_topics(self.config.topics)
        return self.topics

    def get_error_topic(self):
        if self.error_topic is None:
            return self.config.error_topic
        return self.error_topic

    @staticmethod
    def split_topics(topics: str | None) -> list[str]:
        if topics:
            return topics.replace(" ", "").split(",")
        return []

    def get_routes(self) -> set[str]:
        """
        Applies the single message transformers to get target routes (e.g. for the ElasticSearchSinkConnector)
        """
        routes = self.get_topics()
        transforms = self.config.get_transforms()
        for transformer_name in transforms:
            routes = self.apply_transformer(routes, transformer_name)
        return set(routes)

    def apply_transformer(self, indices: list[str], transformer_name: str) -> list[str]:
        transformer_prefix = KafkaConnector.get_transformer_prefix(transformer_name)
        # transformer config without transformer_prefix
        transformer_config = {
            config_name.replace(transformer_prefix, ""): config_value
            for config_name, config_value in self.config.dict().items()
            if KafkaConnector.is_transformer_config(config_name, transformer_prefix)
        }
        transformer_config["topics"] = indices
        try:
            transformer: RouterTransformerConfig = pydantic.parse_obj_as(
                # HACK: https://github.com/samuelcolvin/pydantic/issues/1847
                self._transformers,  # type: ignore[arg-type]
                transformer_config,
            )
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
