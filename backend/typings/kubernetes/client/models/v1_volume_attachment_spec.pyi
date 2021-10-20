import datetime
import typing

import kubernetes.client

class V1VolumeAttachmentSpec:
    attacher: str
    node_name: str
    source: kubernetes.client.V1VolumeAttachmentSource
    def __init__(
        self,
        *,
        attacher: str,
        node_name: str,
        source: kubernetes.client.V1VolumeAttachmentSource
    ) -> None: ...
    def to_dict(self) -> V1VolumeAttachmentSpecDict: ...

class V1VolumeAttachmentSpecDict(typing.TypedDict, total=False):
    attacher: str
    nodeName: str
    source: kubernetes.client.V1VolumeAttachmentSourceDict
