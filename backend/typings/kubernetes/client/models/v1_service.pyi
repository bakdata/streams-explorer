import datetime
import typing

import kubernetes.client

class V1Service:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1ServiceSpec]
    status: typing.Optional[kubernetes.client.V1ServiceStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1ServiceSpec] = ...,
        status: typing.Optional[kubernetes.client.V1ServiceStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1ServiceDict: ...

class V1ServiceDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1ServiceSpecDict]
    status: typing.Optional[kubernetes.client.V1ServiceStatusDict]
