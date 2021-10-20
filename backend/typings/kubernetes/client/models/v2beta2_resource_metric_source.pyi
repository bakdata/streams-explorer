import datetime
import typing

import kubernetes.client

class V2beta2ResourceMetricSource:
    name: str
    target: kubernetes.client.V2beta2MetricTarget
    def __init__(
        self, *, name: str, target: kubernetes.client.V2beta2MetricTarget
    ) -> None: ...
    def to_dict(self) -> V2beta2ResourceMetricSourceDict: ...

class V2beta2ResourceMetricSourceDict(typing.TypedDict, total=False):
    name: str
    target: kubernetes.client.V2beta2MetricTargetDict
