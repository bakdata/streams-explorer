import datetime
import typing

import kubernetes.client

class V2beta2ObjectMetricStatus:
    current: kubernetes.client.V2beta2MetricValueStatus
    described_object: kubernetes.client.V2beta2CrossVersionObjectReference
    metric: kubernetes.client.V2beta2MetricIdentifier
    def __init__(
        self,
        *,
        current: kubernetes.client.V2beta2MetricValueStatus,
        described_object: kubernetes.client.V2beta2CrossVersionObjectReference,
        metric: kubernetes.client.V2beta2MetricIdentifier
    ) -> None: ...
    def to_dict(self) -> V2beta2ObjectMetricStatusDict: ...

class V2beta2ObjectMetricStatusDict(typing.TypedDict, total=False):
    current: kubernetes.client.V2beta2MetricValueStatusDict
    describedObject: kubernetes.client.V2beta2CrossVersionObjectReferenceDict
    metric: kubernetes.client.V2beta2MetricIdentifierDict
