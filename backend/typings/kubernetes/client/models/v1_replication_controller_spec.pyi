import datetime
import typing

import kubernetes.client

class V1ReplicationControllerSpec:
    min_ready_seconds: typing.Optional[int]
    replicas: typing.Optional[int]
    selector: typing.Optional[dict[str, str]]
    template: typing.Optional[kubernetes.client.V1PodTemplateSpec]
    def __init__(
        self,
        *,
        min_ready_seconds: typing.Optional[int] = ...,
        replicas: typing.Optional[int] = ...,
        selector: typing.Optional[dict[str, str]] = ...,
        template: typing.Optional[kubernetes.client.V1PodTemplateSpec] = ...
    ) -> None: ...
    def to_dict(self) -> V1ReplicationControllerSpecDict: ...

class V1ReplicationControllerSpecDict(typing.TypedDict, total=False):
    minReadySeconds: typing.Optional[int]
    replicas: typing.Optional[int]
    selector: typing.Optional[dict[str, str]]
    template: typing.Optional[kubernetes.client.V1PodTemplateSpecDict]
