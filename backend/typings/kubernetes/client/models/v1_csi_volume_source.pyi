import datetime
import typing

import kubernetes.client

class V1CSIVolumeSource:
    driver: str
    fs_type: typing.Optional[str]
    node_publish_secret_ref: typing.Optional[kubernetes.client.V1LocalObjectReference]
    read_only: typing.Optional[bool]
    volume_attributes: typing.Optional[dict[str, str]]
    def __init__(
        self,
        *,
        driver: str,
        fs_type: typing.Optional[str] = ...,
        node_publish_secret_ref: typing.Optional[
            kubernetes.client.V1LocalObjectReference
        ] = ...,
        read_only: typing.Optional[bool] = ...,
        volume_attributes: typing.Optional[dict[str, str]] = ...
    ) -> None: ...
    def to_dict(self) -> V1CSIVolumeSourceDict: ...

class V1CSIVolumeSourceDict(typing.TypedDict, total=False):
    driver: str
    fsType: typing.Optional[str]
    nodePublishSecretRef: typing.Optional[kubernetes.client.V1LocalObjectReferenceDict]
    readOnly: typing.Optional[bool]
    volumeAttributes: typing.Optional[dict[str, str]]
