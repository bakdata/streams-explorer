import datetime
import typing

import kubernetes.client

class V2beta1HorizontalPodAutoscalerList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V2beta1HorizontalPodAutoscaler]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V2beta1HorizontalPodAutoscaler],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V2beta1HorizontalPodAutoscalerListDict: ...

class V2beta1HorizontalPodAutoscalerListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V2beta1HorizontalPodAutoscalerDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
