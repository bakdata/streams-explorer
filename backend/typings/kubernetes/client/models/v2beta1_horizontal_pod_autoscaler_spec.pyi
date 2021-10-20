import datetime
import typing

import kubernetes.client

class V2beta1HorizontalPodAutoscalerSpec:
    max_replicas: int
    metrics: typing.Optional[list[kubernetes.client.V2beta1MetricSpec]]
    min_replicas: typing.Optional[int]
    scale_target_ref: kubernetes.client.V2beta1CrossVersionObjectReference
    def __init__(
        self,
        *,
        max_replicas: int,
        metrics: typing.Optional[list[kubernetes.client.V2beta1MetricSpec]] = ...,
        min_replicas: typing.Optional[int] = ...,
        scale_target_ref: kubernetes.client.V2beta1CrossVersionObjectReference
    ) -> None: ...
    def to_dict(self) -> V2beta1HorizontalPodAutoscalerSpecDict: ...

class V2beta1HorizontalPodAutoscalerSpecDict(typing.TypedDict, total=False):
    maxReplicas: int
    metrics: typing.Optional[list[kubernetes.client.V2beta1MetricSpecDict]]
    minReplicas: typing.Optional[int]
    scaleTargetRef: kubernetes.client.V2beta1CrossVersionObjectReferenceDict
