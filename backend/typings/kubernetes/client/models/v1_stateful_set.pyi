import datetime
import typing

import kubernetes.client

class V1StatefulSet:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1StatefulSetSpec]
    status: typing.Optional[kubernetes.client.V1StatefulSetStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1StatefulSetSpec] = ...,
        status: typing.Optional[kubernetes.client.V1StatefulSetStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1StatefulSetDict: ...

class V1StatefulSetDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1StatefulSetSpecDict]
    status: typing.Optional[kubernetes.client.V1StatefulSetStatusDict]
