import datetime
import typing

import kubernetes.client

class V1beta1CertificateSigningRequest:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta1CertificateSigningRequestSpec]
    status: typing.Optional[kubernetes.client.V1beta1CertificateSigningRequestStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[
            kubernetes.client.V1beta1CertificateSigningRequestSpec
        ] = ...,
        status: typing.Optional[
            kubernetes.client.V1beta1CertificateSigningRequestStatus
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1CertificateSigningRequestDict: ...

class V1beta1CertificateSigningRequestDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta1CertificateSigningRequestSpecDict]
    status: typing.Optional[
        kubernetes.client.V1beta1CertificateSigningRequestStatusDict
    ]
