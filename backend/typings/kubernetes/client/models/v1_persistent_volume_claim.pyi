import datetime
import typing

import kubernetes.client

class V1PersistentVolumeClaim:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1PersistentVolumeClaimSpec]
    status: typing.Optional[kubernetes.client.V1PersistentVolumeClaimStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1PersistentVolumeClaimSpec] = ...,
        status: typing.Optional[kubernetes.client.V1PersistentVolumeClaimStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1PersistentVolumeClaimDict: ...

class V1PersistentVolumeClaimDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1PersistentVolumeClaimSpecDict]
    status: typing.Optional[kubernetes.client.V1PersistentVolumeClaimStatusDict]
