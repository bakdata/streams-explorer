import datetime
import typing

import kubernetes.client

class V1beta1ClusterRole:
    aggregation_rule: typing.Optional[kubernetes.client.V1beta1AggregationRule]
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    rules: typing.Optional[list[kubernetes.client.V1beta1PolicyRule]]
    def __init__(
        self,
        *,
        aggregation_rule: typing.Optional[
            kubernetes.client.V1beta1AggregationRule
        ] = ...,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        rules: typing.Optional[list[kubernetes.client.V1beta1PolicyRule]] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1ClusterRoleDict: ...

class V1beta1ClusterRoleDict(typing.TypedDict, total=False):
    aggregationRule: typing.Optional[kubernetes.client.V1beta1AggregationRuleDict]
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    rules: typing.Optional[list[kubernetes.client.V1beta1PolicyRuleDict]]
