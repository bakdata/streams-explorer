import re
from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseConfig, BaseModel, Extra, Field, PrivateAttr


class RouterTransformerConfig(BaseModel, ABC):
    _type: str = Field(..., alias="type")
    topics: list[str]

    @abstractmethod
    def transform_topic(self, topic: str) -> str:
        ...

    def get_routes(self) -> list[str]:
        return [self.transform_topic(topic) for topic in self.topics]


class RegexRouterTransformerConfig(RouterTransformerConfig):
    _type: Literal["org.apache.kafka.connect.transforms.RegexRouter"] = Field(
        ..., alias="type"
    )
    regex: str | None = None
    replacement: str

    _rx: re.Pattern[str] = PrivateAttr()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.regex is not None:
            self._rx = re.compile(self.regex)
        self.replacement = self.replacement.replace("$", "\\")

    def transform_topic(self, topic: str) -> str:
        return re.sub(self._rx, self.replacement, topic, 1)

    def get_routes(self) -> list[str]:
        if self.regex is not None:
            return super().get_routes()
        return [self.replacement]


class TimestampRouterTransformerConfig(RouterTransformerConfig):
    _type: Literal["org.apache.kafka.connect.transforms.TimestampRouter"] = Field(
        ..., alias="type"
    )
    topic_format: str = Field(..., alias="topic.format")
    timestamp_format: str = Field(..., alias="timestamp.format")

    def transform_topic(self, topic: str) -> str:
        transformed_topic = self.topic_format
        transformed_topic = transformed_topic.replace("${topic}", topic)
        transformed_topic = transformed_topic.replace(
            "${timestamp}", "${" + self.timestamp_format + "}"
        )
        return transformed_topic


# Used as fallback for unknown transforms
class GenericTransformerConfig(RouterTransformerConfig):
    _type: str = Field(..., alias="type")

    class Config(BaseConfig):
        extra = Extra.allow

    def transform_topic(self, topic: str) -> str:
        return topic
