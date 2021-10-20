import datetime
import typing

import kubernetes.client

class V1PodReadinessGate:
    condition_type: str
    def __init__(self, *, condition_type: str) -> None: ...
    def to_dict(self) -> V1PodReadinessGateDict: ...

class V1PodReadinessGateDict(typing.TypedDict, total=False):
    conditionType: str
