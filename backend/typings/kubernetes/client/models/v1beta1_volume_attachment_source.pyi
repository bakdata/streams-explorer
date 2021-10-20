import datetime
import typing

import kubernetes.client

class V1beta1VolumeAttachmentSource:
    inline_volume_spec: typing.Optional[kubernetes.client.V1PersistentVolumeSpec]
    persistent_volume_name: typing.Optional[str]
    def __init__(
        self,
        *,
        inline_volume_spec: typing.Optional[
            kubernetes.client.V1PersistentVolumeSpec
        ] = ...,
        persistent_volume_name: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1VolumeAttachmentSourceDict: ...

class V1beta1VolumeAttachmentSourceDict(typing.TypedDict, total=False):
    inlineVolumeSpec: typing.Optional[kubernetes.client.V1PersistentVolumeSpecDict]
    persistentVolumeName: typing.Optional[str]
