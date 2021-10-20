import datetime
import typing

import kubernetes.client

class V2beta2ExternalMetricSource:
    metric: kubernetes.client.V2beta2MetricIdentifier
    target: kubernetes.client.V2beta2MetricTarget
    def __init__(
        self,
        *,
        metric: kubernetes.client.V2beta2MetricIdentifier,
        target: kubernetes.client.V2beta2MetricTarget
    ) -> None: ...
    def to_dict(self) -> V2beta2ExternalMetricSourceDict: ...

class V2beta2ExternalMetricSourceDict(typing.TypedDict, total=False):
    metric: kubernetes.client.V2beta2MetricIdentifierDict
    target: kubernetes.client.V2beta2MetricTargetDict
