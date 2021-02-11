from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class KafkaConnectorTypesEnum(str, Enum):
    SINK = "sink"
    SOURCE = "source"


@dataclass
class KafkaConnector:
    name: str
    config: dict
    topics: List[str]
    type: Optional[KafkaConnectorTypesEnum] = None
