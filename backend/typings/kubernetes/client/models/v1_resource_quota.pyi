import datetime
import typing

import kubernetes.client

class V1ResourceQuota:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1ResourceQuotaSpec]
    status: typing.Optional[kubernetes.client.V1ResourceQuotaStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1ResourceQuotaSpec] = ...,
        status: typing.Optional[kubernetes.client.V1ResourceQuotaStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1ResourceQuotaDict: ...

class V1ResourceQuotaDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1ResourceQuotaSpecDict]
    status: typing.Optional[kubernetes.client.V1ResourceQuotaStatusDict]
