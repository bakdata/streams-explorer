import datetime
import typing

import kubernetes.client

class NetworkingV1beta1IngressList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.NetworkingV1beta1Ingress]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.NetworkingV1beta1Ingress],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> NetworkingV1beta1IngressListDict: ...

class NetworkingV1beta1IngressListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.NetworkingV1beta1IngressDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
