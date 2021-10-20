import datetime
import typing

import kubernetes.client

class V1beta1VolumeAttachmentList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1beta1VolumeAttachment]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1beta1VolumeAttachment],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1VolumeAttachmentListDict: ...

class V1beta1VolumeAttachmentListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1beta1VolumeAttachmentDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
