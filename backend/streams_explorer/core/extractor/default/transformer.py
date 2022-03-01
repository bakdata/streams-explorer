import re
from abc import ABC, abstractmethod
from typing import List, Literal, Optional, Pattern

from pydantic import BaseConfig, BaseModel, Extra, Field, PrivateAttr


class RouterTransformerConfig(BaseModel, ABC):
    _type: str = Field(..., alias="type")
    topics: List[str]

    @abstractmethod
    def transform_topic(self, topic: str) -> str:
        ...

    def get_routes(self) -> List[str]:
        return [self.transform_topic(topic) for topic in self.topics]


class RegexRouterTransformerConfig(RouterTransformerConfig):
    _type: Literal["org.apache.kafka.connect.transforms.RegexRouter"] = Field(
        ..., alias="type"
    )
    regex: Optional[str] = None
    replacement: str

    _rx: Pattern = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.regex is not None:
            self._rx = re.compile(self.regex)
        self.replacement = self.replacement.replace("$", "\\")

    def get_routes(self) -> List[str]:
        if self.regex is not None:
            return [self.transform_topic(topic) for topic in self.topics]
        return [self.replacement]

    def transform_topic(self, topic: str) -> str:
        return re.sub(self._rx, self.replacement, topic)


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
