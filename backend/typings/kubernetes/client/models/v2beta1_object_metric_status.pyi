import datetime
import typing

import kubernetes.client

class V2beta1ObjectMetricStatus:
    average_value: typing.Optional[str]
    current_value: str
    metric_name: str
    selector: typing.Optional[kubernetes.client.V1LabelSelector]
    target: kubernetes.client.V2beta1CrossVersionObjectReference
    def __init__(
        self,
        *,
        average_value: typing.Optional[str] = ...,
        current_value: str,
        metric_name: str,
        selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...,
        target: kubernetes.client.V2beta1CrossVersionObjectReference
    ) -> None: ...
    def to_dict(self) -> V2beta1ObjectMetricStatusDict: ...

class V2beta1ObjectMetricStatusDict(typing.TypedDict, total=False):
    averageValue: typing.Optional[str]
    currentValue: str
    metricName: str
    selector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    target: kubernetes.client.V2beta1CrossVersionObjectReferenceDict
