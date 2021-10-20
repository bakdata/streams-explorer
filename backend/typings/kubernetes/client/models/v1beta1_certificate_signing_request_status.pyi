import datetime
import typing

import kubernetes.client

class V1beta1CertificateSigningRequestStatus:
    certificate: typing.Optional[str]
    conditions: typing.Optional[
        list[kubernetes.client.V1beta1CertificateSigningRequestCondition]
    ]
    def __init__(
        self,
        *,
        certificate: typing.Optional[str] = ...,
        conditions: typing.Optional[
            list[kubernetes.client.V1beta1CertificateSigningRequestCondition]
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1CertificateSigningRequestStatusDict: ...

class V1beta1CertificateSigningRequestStatusDict(typing.TypedDict, total=False):
    certificate: typing.Optional[str]
    conditions: typing.Optional[
        list[kubernetes.client.V1beta1CertificateSigningRequestConditionDict]
    ]
