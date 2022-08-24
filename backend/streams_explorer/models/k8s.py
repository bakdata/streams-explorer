from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass
class K8sConfig:
    id: str
    name: str
    input_topics: list[str] = field(default_factory=list)  # required for streaming app
    output_topic: str | None = None  # required for streaming app
    error_topic: str | None = None
    input_pattern: str | None = None
    extra_input_topics: list[str] = field(default_factory=list)
    extra_output_topics: list[str] = field(default_factory=list)
    extra_input_patterns: list[str] = field(default_factory=list)
    extra: dict[str, str] = field(default_factory=dict)


class K8sDeploymentUpdateType(str, Enum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"


# Documentation: https://github.com/tomplus/kubernetes_asyncio/blob/11c3eb4d50ae822545572aa7b8c15f7153f65a1c/kubernetes_asyncio/docs/EventsV1Event.md
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

    @staticmethod
    def from_str(reason: str) -> K8sReason:
        try:
            return K8sReason[reason.upper()]
        except KeyError:
            raise NotImplementedError(f"Kubernetes event reason '{reason}' is unknown")
