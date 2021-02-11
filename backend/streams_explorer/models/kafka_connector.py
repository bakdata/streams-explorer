from dataclasses import dataclass
from enum import Enum
from typing import Optional


class KafkaConnectorTypesEnum(str, Enum):
    SINK = "sink"
    SOURCE = "source"


@dataclass
class KafkaConnector:
    name: str
    config: dict
    type: Optional[KafkaConnectorTypesEnum] = None
