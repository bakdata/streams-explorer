import datetime
import typing

import kubernetes.client

class V1ConfigMap:
    api_version: typing.Optional[str]
    binary_data: typing.Optional[dict[str, str]]
    data: typing.Optional[dict[str, str]]
    immutable: typing.Optional[bool]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        binary_data: typing.Optional[dict[str, str]] = ...,
        data: typing.Optional[dict[str, str]] = ...,
        immutable: typing.Optional[bool] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1ConfigMapDict: ...

class V1ConfigMapDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    binaryData: typing.Optional[dict[str, str]]
    data: typing.Optional[dict[str, str]]
    immutable: typing.Optional[bool]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
