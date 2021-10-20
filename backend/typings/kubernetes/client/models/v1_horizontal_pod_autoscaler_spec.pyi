import datetime
import typing

import kubernetes.client

class V1HorizontalPodAutoscalerSpec:
    max_replicas: int
    min_replicas: typing.Optional[int]
    scale_target_ref: kubernetes.client.V1CrossVersionObjectReference
    target_cpu_utilization_percentage: typing.Optional[int]
    def __init__(
        self,
        *,
        max_replicas: int,
        min_replicas: typing.Optional[int] = ...,
        scale_target_ref: kubernetes.client.V1CrossVersionObjectReference,
        target_cpu_utilization_percentage: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1HorizontalPodAutoscalerSpecDict: ...

class V1HorizontalPodAutoscalerSpecDict(typing.TypedDict, total=False):
    maxReplicas: int
    minReplicas: typing.Optional[int]
    scaleTargetRef: kubernetes.client.V1CrossVersionObjectReferenceDict
    targetCPUUtilizationPercentage: typing.Optional[int]
