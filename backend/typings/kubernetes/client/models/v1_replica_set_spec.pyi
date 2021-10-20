import datetime
import typing

import kubernetes.client

class V1ReplicaSetSpec:
    min_ready_seconds: typing.Optional[int]
    replicas: typing.Optional[int]
    selector: kubernetes.client.V1LabelSelector
    template: typing.Optional[kubernetes.client.V1PodTemplateSpec]
    def __init__(
        self,
        *,
        min_ready_seconds: typing.Optional[int] = ...,
        replicas: typing.Optional[int] = ...,
        selector: kubernetes.client.V1LabelSelector,
        template: typing.Optional[kubernetes.client.V1PodTemplateSpec] = ...
    ) -> None: ...
    def to_dict(self) -> V1ReplicaSetSpecDict: ...

class V1ReplicaSetSpecDict(typing.TypedDict, total=False):
    minReadySeconds: typing.Optional[int]
    replicas: typing.Optional[int]
    selector: kubernetes.client.V1LabelSelectorDict
    template: typing.Optional[kubernetes.client.V1PodTemplateSpecDict]
