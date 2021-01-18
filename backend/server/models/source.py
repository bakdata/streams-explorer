from dataclasses import dataclass


@dataclass
class Source:
    name: str
    target: str
    node_type: str = "source"
