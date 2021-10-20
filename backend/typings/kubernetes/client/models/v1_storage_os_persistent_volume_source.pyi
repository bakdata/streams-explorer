import datetime
import typing

import kubernetes.client

class V1StorageOSPersistentVolumeSource:
    fs_type: typing.Optional[str]
    read_only: typing.Optional[bool]
    secret_ref: typing.Optional[kubernetes.client.V1ObjectReference]
    volume_name: typing.Optional[str]
    volume_namespace: typing.Optional[str]
    def __init__(
        self,
        *,
        fs_type: typing.Optional[str] = ...,
        read_only: typing.Optional[bool] = ...,
        secret_ref: typing.Optional[kubernetes.client.V1ObjectReference] = ...,
        volume_name: typing.Optional[str] = ...,
        volume_namespace: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1StorageOSPersistentVolumeSourceDict: ...

class V1StorageOSPersistentVolumeSourceDict(typing.TypedDict, total=False):
    fsType: typing.Optional[str]
    readOnly: typing.Optional[bool]
    secretRef: typing.Optional[kubernetes.client.V1ObjectReferenceDict]
    volumeName: typing.Optional[str]
    volumeNamespace: typing.Optional[str]
