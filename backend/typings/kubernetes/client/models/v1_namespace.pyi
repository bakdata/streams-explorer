import datetime
import typing

import kubernetes.client

class V1Namespace:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1NamespaceSpec]
    status: typing.Optional[kubernetes.client.V1NamespaceStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1NamespaceSpec] = ...,
        status: typing.Optional[kubernetes.client.V1NamespaceStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1NamespaceDict: ...

class V1NamespaceDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1NamespaceSpecDict]
    status: typing.Optional[kubernetes.client.V1NamespaceStatusDict]
