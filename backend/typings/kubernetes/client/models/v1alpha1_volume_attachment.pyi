import datetime
import typing

import kubernetes.client

class V1alpha1VolumeAttachment:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha1VolumeAttachmentSpec
    status: typing.Optional[kubernetes.client.V1alpha1VolumeAttachmentStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: kubernetes.client.V1alpha1VolumeAttachmentSpec,
        status: typing.Optional[kubernetes.client.V1alpha1VolumeAttachmentStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1VolumeAttachmentDict: ...

class V1alpha1VolumeAttachmentDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha1VolumeAttachmentSpecDict
    status: typing.Optional[kubernetes.client.V1alpha1VolumeAttachmentStatusDict]
