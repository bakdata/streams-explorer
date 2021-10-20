import datetime
import typing

import kubernetes.client

class V1APIService:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1APIServiceSpec]
    status: typing.Optional[kubernetes.client.V1APIServiceStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1APIServiceSpec] = ...,
        status: typing.Optional[kubernetes.client.V1APIServiceStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1APIServiceDict: ...

class V1APIServiceDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1APIServiceSpecDict]
    status: typing.Optional[kubernetes.client.V1APIServiceStatusDict]
