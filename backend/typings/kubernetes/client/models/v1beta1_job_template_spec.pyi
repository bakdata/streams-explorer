import datetime
import typing

import kubernetes.client

class V1beta1JobTemplateSpec:
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1JobSpec]
    def __init__(
        self,
        *,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1JobSpec] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1JobTemplateSpecDict: ...

class V1beta1JobTemplateSpecDict(typing.TypedDict, total=False):
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1JobSpecDict]
