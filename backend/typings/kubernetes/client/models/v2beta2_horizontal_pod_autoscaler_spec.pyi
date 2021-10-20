import datetime
import typing

import kubernetes.client

class V2beta2HorizontalPodAutoscalerSpec:
    behavior: typing.Optional[kubernetes.client.V2beta2HorizontalPodAutoscalerBehavior]
    max_replicas: int
    metrics: typing.Optional[list[kubernetes.client.V2beta2MetricSpec]]
    min_replicas: typing.Optional[int]
    scale_target_ref: kubernetes.client.V2beta2CrossVersionObjectReference
    def __init__(
        self,
        *,
        behavior: typing.Optional[
            kubernetes.client.V2beta2HorizontalPodAutoscalerBehavior
        ] = ...,
        max_replicas: int,
        metrics: typing.Optional[list[kubernetes.client.V2beta2MetricSpec]] = ...,
        min_replicas: typing.Optional[int] = ...,
        scale_target_ref: kubernetes.client.V2beta2CrossVersionObjectReference
    ) -> None: ...
    def to_dict(self) -> V2beta2HorizontalPodAutoscalerSpecDict: ...

class V2beta2HorizontalPodAutoscalerSpecDict(typing.TypedDict, total=False):
    behavior: typing.Optional[
        kubernetes.client.V2beta2HorizontalPodAutoscalerBehaviorDict
    ]
    maxReplicas: int
    metrics: typing.Optional[list[kubernetes.client.V2beta2MetricSpecDict]]
    minReplicas: typing.Optional[int]
    scaleTargetRef: kubernetes.client.V2beta2CrossVersionObjectReferenceDict
