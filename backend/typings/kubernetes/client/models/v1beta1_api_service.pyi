import datetime
import typing

import kubernetes.client

class V1beta1APIService:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta1APIServiceSpec]
    status: typing.Optional[kubernetes.client.V1beta1APIServiceStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1beta1APIServiceSpec] = ...,
        status: typing.Optional[kubernetes.client.V1beta1APIServiceStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1APIServiceDict: ...

class V1beta1APIServiceDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta1APIServiceSpecDict]
    status: typing.Optional[kubernetes.client.V1beta1APIServiceStatusDict]
