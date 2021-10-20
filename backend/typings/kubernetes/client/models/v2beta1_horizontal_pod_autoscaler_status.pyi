import datetime
import typing

import kubernetes.client

class V2beta1HorizontalPodAutoscalerStatus:
    conditions: list[kubernetes.client.V2beta1HorizontalPodAutoscalerCondition]
    current_metrics: typing.Optional[list[kubernetes.client.V2beta1MetricStatus]]
    current_replicas: int
    desired_replicas: int
    last_scale_time: typing.Optional[datetime.datetime]
    observed_generation: typing.Optional[int]
    def __init__(
        self,
        *,
        conditions: list[kubernetes.client.V2beta1HorizontalPodAutoscalerCondition],
        current_metrics: typing.Optional[
            list[kubernetes.client.V2beta1MetricStatus]
        ] = ...,
        current_replicas: int,
        desired_replicas: int,
        last_scale_time: typing.Optional[datetime.datetime] = ...,
        observed_generation: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V2beta1HorizontalPodAutoscalerStatusDict: ...

class V2beta1HorizontalPodAutoscalerStatusDict(typing.TypedDict, total=False):
    conditions: list[kubernetes.client.V2beta1HorizontalPodAutoscalerConditionDict]
    currentMetrics: typing.Optional[list[kubernetes.client.V2beta1MetricStatusDict]]
    currentReplicas: int
    desiredReplicas: int
    lastScaleTime: typing.Optional[datetime.datetime]
    observedGeneration: typing.Optional[int]
