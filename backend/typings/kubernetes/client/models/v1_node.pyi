import datetime
import typing

import kubernetes.client

class V1Node:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1NodeSpec]
    status: typing.Optional[kubernetes.client.V1NodeStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1NodeSpec] = ...,
        status: typing.Optional[kubernetes.client.V1NodeStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1NodeDict: ...

class V1NodeDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1NodeSpecDict]
    status: typing.Optional[kubernetes.client.V1NodeStatusDict]
