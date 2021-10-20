import datetime
import typing

import kubernetes.client

class V1PreferredSchedulingTerm:
    preference: kubernetes.client.V1NodeSelectorTerm
    weight: int
    def __init__(
        self, *, preference: kubernetes.client.V1NodeSelectorTerm, weight: int
    ) -> None: ...
    def to_dict(self) -> V1PreferredSchedulingTermDict: ...

class V1PreferredSchedulingTermDict(typing.TypedDict, total=False):
    preference: kubernetes.client.V1NodeSelectorTermDict
    weight: int
