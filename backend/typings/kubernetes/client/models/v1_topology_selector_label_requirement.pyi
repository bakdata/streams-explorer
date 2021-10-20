import datetime
import typing

import kubernetes.client

class V1TopologySelectorLabelRequirement:
    key: str
    values: list[str]
    def __init__(self, *, key: str, values: list[str]) -> None: ...
    def to_dict(self) -> V1TopologySelectorLabelRequirementDict: ...

class V1TopologySelectorLabelRequirementDict(typing.TypedDict, total=False):
    key: str
    values: list[str]
