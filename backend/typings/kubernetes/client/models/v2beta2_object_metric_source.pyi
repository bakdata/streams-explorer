import datetime
import typing

import kubernetes.client

class V2beta2ObjectMetricSource:
    described_object: kubernetes.client.V2beta2CrossVersionObjectReference
    metric: kubernetes.client.V2beta2MetricIdentifier
    target: kubernetes.client.V2beta2MetricTarget
    def __init__(
        self,
        *,
        described_object: kubernetes.client.V2beta2CrossVersionObjectReference,
        metric: kubernetes.client.V2beta2MetricIdentifier,
        target: kubernetes.client.V2beta2MetricTarget
    ) -> None: ...
    def to_dict(self) -> V2beta2ObjectMetricSourceDict: ...

class V2beta2ObjectMetricSourceDict(typing.TypedDict, total=False):
    describedObject: kubernetes.client.V2beta2CrossVersionObjectReferenceDict
    metric: kubernetes.client.V2beta2MetricIdentifierDict
    target: kubernetes.client.V2beta2MetricTargetDict
