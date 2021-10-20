import datetime
import typing

import kubernetes.client

class V1beta1VolumeAttachmentStatus:
    attach_error: typing.Optional[kubernetes.client.V1beta1VolumeError]
    attached: bool
    attachment_metadata: typing.Optional[dict[str, str]]
    detach_error: typing.Optional[kubernetes.client.V1beta1VolumeError]
    def __init__(
        self,
        *,
        attach_error: typing.Optional[kubernetes.client.V1beta1VolumeError] = ...,
        attached: bool,
        attachment_metadata: typing.Optional[dict[str, str]] = ...,
        detach_error: typing.Optional[kubernetes.client.V1beta1VolumeError] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1VolumeAttachmentStatusDict: ...

class V1beta1VolumeAttachmentStatusDict(typing.TypedDict, total=False):
    attachError: typing.Optional[kubernetes.client.V1beta1VolumeErrorDict]
    attached: bool
    attachmentMetadata: typing.Optional[dict[str, str]]
    detachError: typing.Optional[kubernetes.client.V1beta1VolumeErrorDict]
