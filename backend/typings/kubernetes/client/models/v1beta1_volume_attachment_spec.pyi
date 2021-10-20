import datetime
import typing

import kubernetes.client

class V1beta1VolumeAttachmentSpec:
    attacher: str
    node_name: str
    source: kubernetes.client.V1beta1VolumeAttachmentSource
    def __init__(
        self,
        *,
        attacher: str,
        node_name: str,
        source: kubernetes.client.V1beta1VolumeAttachmentSource
    ) -> None: ...
    def to_dict(self) -> V1beta1VolumeAttachmentSpecDict: ...

class V1beta1VolumeAttachmentSpecDict(typing.TypedDict, total=False):
    attacher: str
    nodeName: str
    source: kubernetes.client.V1beta1VolumeAttachmentSourceDict
