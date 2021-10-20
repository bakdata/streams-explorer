import datetime
import typing

import kubernetes.client

class V1ComponentStatus:
    api_version: typing.Optional[str]
    conditions: typing.Optional[list[kubernetes.client.V1ComponentCondition]]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        conditions: typing.Optional[list[kubernetes.client.V1ComponentCondition]] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1ComponentStatusDict: ...

class V1ComponentStatusDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    conditions: typing.Optional[list[kubernetes.client.V1ComponentConditionDict]]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
