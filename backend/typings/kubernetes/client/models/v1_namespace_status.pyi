import datetime
import typing

import kubernetes.client

class V1NamespaceStatus:
    conditions: typing.Optional[list[kubernetes.client.V1NamespaceCondition]]
    phase: typing.Optional[str]
    def __init__(
        self,
        *,
        conditions: typing.Optional[list[kubernetes.client.V1NamespaceCondition]] = ...,
        phase: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1NamespaceStatusDict: ...

class V1NamespaceStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1NamespaceConditionDict]]
    phase: typing.Optional[str]
