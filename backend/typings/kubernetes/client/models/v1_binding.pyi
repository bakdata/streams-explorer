import datetime
import typing

import kubernetes.client

class V1Binding:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    target: kubernetes.client.V1ObjectReference
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        target: kubernetes.client.V1ObjectReference
    ) -> None: ...
    def to_dict(self) -> V1BindingDict: ...

class V1BindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    target: kubernetes.client.V1ObjectReferenceDict
