import datetime
import typing

import kubernetes.client

class V1beta1CertificateSigningRequestList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1beta1CertificateSigningRequest]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1beta1CertificateSigningRequest],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1CertificateSigningRequestListDict: ...

class V1beta1CertificateSigningRequestListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1beta1CertificateSigningRequestDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
