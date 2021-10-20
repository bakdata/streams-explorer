import datetime
import typing

import kubernetes.client

class V1Status:
    api_version: typing.Optional[str]
    code: typing.Optional[int]
    details: typing.Optional[kubernetes.client.V1StatusDetails]
    kind: typing.Optional[str]
    message: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    reason: typing.Optional[str]
    status: typing.Optional[str]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        code: typing.Optional[int] = ...,
        details: typing.Optional[kubernetes.client.V1StatusDetails] = ...,
        kind: typing.Optional[str] = ...,
        message: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...,
        reason: typing.Optional[str] = ...,
        status: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1StatusDict: ...

class V1StatusDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    code: typing.Optional[int]
    details: typing.Optional[kubernetes.client.V1StatusDetailsDict]
    kind: typing.Optional[str]
    message: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
    reason: typing.Optional[str]
    status: typing.Optional[str]
