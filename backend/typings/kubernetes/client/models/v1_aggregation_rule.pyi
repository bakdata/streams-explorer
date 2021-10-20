import datetime
import typing

import kubernetes.client

class V1AggregationRule:
    cluster_role_selectors: typing.Optional[list[kubernetes.client.V1LabelSelector]]
    def __init__(
        self,
        *,
        cluster_role_selectors: typing.Optional[
            list[kubernetes.client.V1LabelSelector]
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1AggregationRuleDict: ...

class V1AggregationRuleDict(typing.TypedDict, total=False):
    clusterRoleSelectors: typing.Optional[list[kubernetes.client.V1LabelSelectorDict]]
