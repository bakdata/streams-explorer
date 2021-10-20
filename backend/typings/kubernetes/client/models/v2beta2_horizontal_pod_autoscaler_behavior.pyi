import datetime
import typing

import kubernetes.client

class V2beta2HorizontalPodAutoscalerBehavior:
    scale_down: typing.Optional[kubernetes.client.V2beta2HPAScalingRules]
    scale_up: typing.Optional[kubernetes.client.V2beta2HPAScalingRules]
    def __init__(
        self,
        *,
        scale_down: typing.Optional[kubernetes.client.V2beta2HPAScalingRules] = ...,
        scale_up: typing.Optional[kubernetes.client.V2beta2HPAScalingRules] = ...
    ) -> None: ...
    def to_dict(self) -> V2beta2HorizontalPodAutoscalerBehaviorDict: ...

class V2beta2HorizontalPodAutoscalerBehaviorDict(typing.TypedDict, total=False):
    scaleDown: typing.Optional[kubernetes.client.V2beta2HPAScalingRulesDict]
    scaleUp: typing.Optional[kubernetes.client.V2beta2HPAScalingRulesDict]
