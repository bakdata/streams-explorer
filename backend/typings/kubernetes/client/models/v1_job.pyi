import datetime
import typing

import kubernetes.client

class V1Job:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1JobSpec]
    status: typing.Optional[kubernetes.client.V1JobStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1JobSpec] = ...,
        status: typing.Optional[kubernetes.client.V1JobStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1JobDict: ...

class V1JobDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1JobSpecDict]
    status: typing.Optional[kubernetes.client.V1JobStatusDict]
