import datetime
import typing

import kubernetes.client

class V1CinderPersistentVolumeSource:
    fs_type: typing.Optional[str]
    read_only: typing.Optional[bool]
    secret_ref: typing.Optional[kubernetes.client.V1SecretReference]
    volume_id: str
    def __init__(
        self,
        *,
        fs_type: typing.Optional[str] = ...,
        read_only: typing.Optional[bool] = ...,
        secret_ref: typing.Optional[kubernetes.client.V1SecretReference] = ...,
        volume_id: str
    ) -> None: ...
    def to_dict(self) -> V1CinderPersistentVolumeSourceDict: ...

class V1CinderPersistentVolumeSourceDict(typing.TypedDict, total=False):
    fsType: typing.Optional[str]
    readOnly: typing.Optional[bool]
    secretRef: typing.Optional[kubernetes.client.V1SecretReferenceDict]
    volumeID: str
