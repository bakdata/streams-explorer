import datetime
import typing

import kubernetes.client

class V2alpha1JobTemplateSpec:
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1JobSpec]
    def __init__(
        self,
        *,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1JobSpec] = ...
    ) -> None: ...
    def to_dict(self) -> V2alpha1JobTemplateSpecDict: ...

class V2alpha1JobTemplateSpecDict(typing.TypedDict, total=False):
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1JobSpecDict]
