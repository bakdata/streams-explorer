import datetime
import typing

import kubernetes.client

class V1alpha1FlowSchemaList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1FlowSchema]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1alpha1FlowSchema],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1FlowSchemaListDict: ...

class V1alpha1FlowSchemaListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1FlowSchemaDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
