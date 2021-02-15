from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class KafkaConnectorTypesEnum(str, Enum):
    SINK = "sink"
    SOURCE = "source"


@dataclass
class KafkaConnector:
    name: str
    type: KafkaConnectorTypesEnum
    topics: List[str]
    config: dict
    error_topic: Optional[str] = None
