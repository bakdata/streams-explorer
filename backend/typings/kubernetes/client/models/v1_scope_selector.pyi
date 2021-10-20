import datetime
import typing

import kubernetes.client

class V1ScopeSelector:
    match_expressions: typing.Optional[
        list[kubernetes.client.V1ScopedResourceSelectorRequirement]
    ]
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[
            list[kubernetes.client.V1ScopedResourceSelectorRequirement]
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1ScopeSelectorDict: ...

class V1ScopeSelectorDict(typing.TypedDict, total=False):
    matchExpressions: typing.Optional[
        list[kubernetes.client.V1ScopedResourceSelectorRequirementDict]
    ]
