import datetime
import typing

import kubernetes.client

class V1alpha1FlowSchema:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1alpha1FlowSchemaSpec]
    status: typing.Optional[kubernetes.client.V1alpha1FlowSchemaStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1alpha1FlowSchemaSpec] = ...,
        status: typing.Optional[kubernetes.client.V1alpha1FlowSchemaStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1FlowSchemaDict: ...

class V1alpha1FlowSchemaDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1alpha1FlowSchemaSpecDict]
    status: typing.Optional[kubernetes.client.V1alpha1FlowSchemaStatusDict]
