import datetime
import typing

import kubernetes.client

class V1alpha1RuntimeClassList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1RuntimeClass]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1alpha1RuntimeClass],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1RuntimeClassListDict: ...

class V1alpha1RuntimeClassListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1RuntimeClassDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
