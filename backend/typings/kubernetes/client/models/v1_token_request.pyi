import datetime
import typing

import kubernetes.client

class V1TokenRequest:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1TokenRequestSpec
    status: typing.Optional[kubernetes.client.V1TokenRequestStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: kubernetes.client.V1TokenRequestSpec,
        status: typing.Optional[kubernetes.client.V1TokenRequestStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1TokenRequestDict: ...

class V1TokenRequestDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1TokenRequestSpecDict
    status: typing.Optional[kubernetes.client.V1TokenRequestStatusDict]
