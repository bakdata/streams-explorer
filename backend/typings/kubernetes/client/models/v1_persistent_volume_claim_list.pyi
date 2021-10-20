import datetime
import typing

import kubernetes.client

class V1PersistentVolumeClaimList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1PersistentVolumeClaim]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1PersistentVolumeClaim],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1PersistentVolumeClaimListDict: ...

class V1PersistentVolumeClaimListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1PersistentVolumeClaimDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
