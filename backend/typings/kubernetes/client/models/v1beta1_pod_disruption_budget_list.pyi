import datetime
import typing

import kubernetes.client

class V1beta1PodDisruptionBudgetList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1beta1PodDisruptionBudget]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1beta1PodDisruptionBudget],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1PodDisruptionBudgetListDict: ...

class V1beta1PodDisruptionBudgetListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1beta1PodDisruptionBudgetDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
