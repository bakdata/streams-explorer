from enum import Enum
from typing import List, Optional

from pydantic import BaseConfig, BaseModel, Extra


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
    topics: Optional[
        List[str]
    ]  # Deprecated please override get_topics for your kafka connector

    def get_topics(self) -> List[str]:
        """
        Override in your kafka connector. Use the config to retrieve and parse the topics.
        This implementation only ensures the support of (older) plugins that use the deprecated topics field.
        """

        return self.topics
