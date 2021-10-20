import datetime
import typing

import kubernetes.client

class V1DaemonSet:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1DaemonSetSpec]
    status: typing.Optional[kubernetes.client.V1DaemonSetStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1DaemonSetSpec] = ...,
        status: typing.Optional[kubernetes.client.V1DaemonSetStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1DaemonSetDict: ...

class V1DaemonSetDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1DaemonSetSpecDict]
    status: typing.Optional[kubernetes.client.V1DaemonSetStatusDict]
