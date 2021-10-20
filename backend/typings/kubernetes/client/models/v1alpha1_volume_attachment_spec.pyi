import datetime
import typing

import kubernetes.client

class V1alpha1VolumeAttachmentSpec:
    attacher: str
    node_name: str
    source: kubernetes.client.V1alpha1VolumeAttachmentSource
    def __init__(
        self,
        *,
        attacher: str,
        node_name: str,
        source: kubernetes.client.V1alpha1VolumeAttachmentSource
    ) -> None: ...
    def to_dict(self) -> V1alpha1VolumeAttachmentSpecDict: ...

class V1alpha1VolumeAttachmentSpecDict(typing.TypedDict, total=False):
    attacher: str
    nodeName: str
    source: kubernetes.client.V1alpha1VolumeAttachmentSourceDict
