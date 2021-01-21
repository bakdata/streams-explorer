from dataclasses import dataclass
from typing import List


@dataclass
class KafkaConnector:
    name: str
    topics: List[str]
    config: dict
