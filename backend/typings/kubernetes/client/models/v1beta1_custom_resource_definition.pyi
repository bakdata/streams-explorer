import datetime
import typing

import kubernetes.client

class V1beta1CustomResourceDefinition:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1CustomResourceDefinitionSpec
    status: typing.Optional[kubernetes.client.V1beta1CustomResourceDefinitionStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: kubernetes.client.V1beta1CustomResourceDefinitionSpec,
        status: typing.Optional[
            kubernetes.client.V1beta1CustomResourceDefinitionStatus
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1CustomResourceDefinitionDict: ...

class V1beta1CustomResourceDefinitionDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1CustomResourceDefinitionSpecDict
    status: typing.Optional[kubernetes.client.V1beta1CustomResourceDefinitionStatusDict]
