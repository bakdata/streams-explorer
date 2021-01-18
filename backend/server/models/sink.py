from dataclasses import dataclass


@dataclass
class Sink:
    name: str
    source: str
    node_type: str = "sink"
