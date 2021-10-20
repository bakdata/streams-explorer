import datetime
import typing

import kubernetes.client

class V2beta2HorizontalPodAutoscaler:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V2beta2HorizontalPodAutoscalerSpec]
    status: typing.Optional[kubernetes.client.V2beta2HorizontalPodAutoscalerStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[
            kubernetes.client.V2beta2HorizontalPodAutoscalerSpec
        ] = ...,
        status: typing.Optional[
            kubernetes.client.V2beta2HorizontalPodAutoscalerStatus
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V2beta2HorizontalPodAutoscalerDict: ...

class V2beta2HorizontalPodAutoscalerDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V2beta2HorizontalPodAutoscalerSpecDict]
    status: typing.Optional[kubernetes.client.V2beta2HorizontalPodAutoscalerStatusDict]
