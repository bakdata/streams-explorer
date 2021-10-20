import datetime
import typing

import kubernetes.client

class V1alpha1VolumeAttachmentStatus:
    attach_error: typing.Optional[kubernetes.client.V1alpha1VolumeError]
    attached: bool
    attachment_metadata: typing.Optional[dict[str, str]]
    detach_error: typing.Optional[kubernetes.client.V1alpha1VolumeError]
    def __init__(
        self,
        *,
        attach_error: typing.Optional[kubernetes.client.V1alpha1VolumeError] = ...,
        attached: bool,
        attachment_metadata: typing.Optional[dict[str, str]] = ...,
        detach_error: typing.Optional[kubernetes.client.V1alpha1VolumeError] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1VolumeAttachmentStatusDict: ...

class V1alpha1VolumeAttachmentStatusDict(typing.TypedDict, total=False):
    attachError: typing.Optional[kubernetes.client.V1alpha1VolumeErrorDict]
    attached: bool
    attachmentMetadata: typing.Optional[dict[str, str]]
    detachError: typing.Optional[kubernetes.client.V1alpha1VolumeErrorDict]
