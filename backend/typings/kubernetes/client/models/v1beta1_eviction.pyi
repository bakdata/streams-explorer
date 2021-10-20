import datetime
import typing

import kubernetes.client

class V1beta1Eviction:
    api_version: typing.Optional[str]
    delete_options: typing.Optional[kubernetes.client.V1DeleteOptions]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        delete_options: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1EvictionDict: ...

class V1beta1EvictionDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    deleteOptions: typing.Optional[kubernetes.client.V1DeleteOptionsDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
