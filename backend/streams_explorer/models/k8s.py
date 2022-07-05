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


class K8sDeploymentUpdateType(str, Enum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"


class K8sEventType(str, Enum):
    NORMAL = "Normal"
    WARNING = "Warning"


class K8sReason(str, Enum):
    UNKNOWN = "Unknown"

    # Container event reason list
    CREATED = "Created"
    STARTED = "Started"
    FAILED = "Failed"
    KILLING = "Killing"
    PREEMPTING = "Preempting"
    BACKOFF = "BackOff"
    EXCEEDEDGRACEPERIOD = "ExceededGracePeriod"

    # Image event reason list
    PULLING = "Pulling"
    PULLED = "Pulled"

    # TODO:? SuccessfulCreate | ScalingReplicaSet | ...

    @staticmethod
    def from_str(reason: str):
        try:
            return K8sReason[reason.upper()]
        except KeyError:
            raise NotImplementedError(f"Kubernetes event reason '{reason}' is unknown")
