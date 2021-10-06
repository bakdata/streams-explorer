from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class K8sConfig:
    name: str
    input_topics: List[str] = field(default_factory=list)
    output_topic: Optional[str] = None
    error_topic: Optional[str] = None
    extra_input_topics: List[str] = field(default_factory=list)
    extra_output_topics: List[str] = field(default_factory=list)
    extra: Dict[str, str] = field(default_factory=dict)
