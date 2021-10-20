import datetime
import typing

import kubernetes.client

class V1CephFSPersistentVolumeSource:
    monitors: list[str]
    path: typing.Optional[str]
    read_only: typing.Optional[bool]
    secret_file: typing.Optional[str]
    secret_ref: typing.Optional[kubernetes.client.V1SecretReference]
    user: typing.Optional[str]
    def __init__(
        self,
        *,
        monitors: list[str],
        path: typing.Optional[str] = ...,
        read_only: typing.Optional[bool] = ...,
        secret_file: typing.Optional[str] = ...,
        secret_ref: typing.Optional[kubernetes.client.V1SecretReference] = ...,
        user: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1CephFSPersistentVolumeSourceDict: ...

class V1CephFSPersistentVolumeSourceDict(typing.TypedDict, total=False):
    monitors: list[str]
    path: typing.Optional[str]
    readOnly: typing.Optional[bool]
    secretFile: typing.Optional[str]
    secretRef: typing.Optional[kubernetes.client.V1SecretReferenceDict]
    user: typing.Optional[str]
