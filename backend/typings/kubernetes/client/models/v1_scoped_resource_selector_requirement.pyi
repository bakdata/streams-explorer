import datetime
import typing

import kubernetes.client

class V1ScopedResourceSelectorRequirement:
    operator: str
    scope_name: str
    values: typing.Optional[list[str]]
    def __init__(
        self,
        *,
        operator: str,
        scope_name: str,
        values: typing.Optional[list[str]] = ...
    ) -> None: ...
    def to_dict(self) -> V1ScopedResourceSelectorRequirementDict: ...

class V1ScopedResourceSelectorRequirementDict(typing.TypedDict, total=False):
    operator: str
    scopeName: str
    values: typing.Optional[list[str]]
