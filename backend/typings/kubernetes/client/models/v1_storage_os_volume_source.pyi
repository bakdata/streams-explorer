import datetime
import typing

import kubernetes.client

class V1StorageOSVolumeSource:
    fs_type: typing.Optional[str]
    read_only: typing.Optional[bool]
    secret_ref: typing.Optional[kubernetes.client.V1LocalObjectReference]
    volume_name: typing.Optional[str]
    volume_namespace: typing.Optional[str]
    def __init__(
        self,
        *,
        fs_type: typing.Optional[str] = ...,
        read_only: typing.Optional[bool] = ...,
        secret_ref: typing.Optional[kubernetes.client.V1LocalObjectReference] = ...,
        volume_name: typing.Optional[str] = ...,
        volume_namespace: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1StorageOSVolumeSourceDict: ...

class V1StorageOSVolumeSourceDict(typing.TypedDict, total=False):
    fsType: typing.Optional[str]
    readOnly: typing.Optional[bool]
    secretRef: typing.Optional[kubernetes.client.V1LocalObjectReferenceDict]
    volumeName: typing.Optional[str]
    volumeNamespace: typing.Optional[str]
