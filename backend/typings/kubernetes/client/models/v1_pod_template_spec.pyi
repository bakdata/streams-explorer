import datetime
import typing

import kubernetes.client

class V1PodTemplateSpec:
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1PodSpec]
    def __init__(
        self,
        *,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1PodSpec] = ...
    ) -> None: ...
    def to_dict(self) -> V1PodTemplateSpecDict: ...

class V1PodTemplateSpecDict(typing.TypedDict, total=False):
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1PodSpecDict]
