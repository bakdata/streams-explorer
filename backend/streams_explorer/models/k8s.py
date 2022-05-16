from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


@dataclass
class K8sConfig:
    id: str
    name: str
    input_topics: List[str] = field(default_factory=list)  # required for streaming app
    output_topic: Optional[str] = None  # required for streaming app
    error_topic: Optional[str] = None
    input_pattern: Optional[str] = None
    extra_input_topics: List[str] = field(default_factory=list)
    extra_output_topics: List[str] = field(default_factory=list)
    extra_input_patterns: List[str] = field(default_factory=list)
    extra: Dict[str, str] = field(default_factory=dict)


class K8sEventType(str, Enum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"
