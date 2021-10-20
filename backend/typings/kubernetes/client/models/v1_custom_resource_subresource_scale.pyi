import datetime
import typing

import kubernetes.client

class V1CustomResourceSubresourceScale:
    label_selector_path: typing.Optional[str]
    spec_replicas_path: str
    status_replicas_path: str
    def __init__(
        self,
        *,
        label_selector_path: typing.Optional[str] = ...,
        spec_replicas_path: str,
        status_replicas_path: str
    ) -> None: ...
    def to_dict(self) -> V1CustomResourceSubresourceScaleDict: ...

class V1CustomResourceSubresourceScaleDict(typing.TypedDict, total=False):
    labelSelectorPath: typing.Optional[str]
    specReplicasPath: str
    statusReplicasPath: str
