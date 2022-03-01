from abc import abstractmethod
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

    @abstractmethod
    def get_topics(self) -> List[str]:
        ...
