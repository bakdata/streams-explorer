import datetime
import typing

import kubernetes.client

class V2beta2PodsMetricStatus:
    current: kubernetes.client.V2beta2MetricValueStatus
    metric: kubernetes.client.V2beta2MetricIdentifier
    def __init__(
        self,
        *,
        current: kubernetes.client.V2beta2MetricValueStatus,
        metric: kubernetes.client.V2beta2MetricIdentifier
    ) -> None: ...
    def to_dict(self) -> V2beta2PodsMetricStatusDict: ...

class V2beta2PodsMetricStatusDict(typing.TypedDict, total=False):
    current: kubernetes.client.V2beta2MetricValueStatusDict
    metric: kubernetes.client.V2beta2MetricIdentifierDict
