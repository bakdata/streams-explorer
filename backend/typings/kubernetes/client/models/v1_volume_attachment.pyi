import datetime
import typing

import kubernetes.client

class V1VolumeAttachment:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1VolumeAttachmentSpec
    status: typing.Optional[kubernetes.client.V1VolumeAttachmentStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: kubernetes.client.V1VolumeAttachmentSpec,
        status: typing.Optional[kubernetes.client.V1VolumeAttachmentStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1VolumeAttachmentDict: ...

class V1VolumeAttachmentDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1VolumeAttachmentSpecDict
    status: typing.Optional[kubernetes.client.V1VolumeAttachmentStatusDict]
