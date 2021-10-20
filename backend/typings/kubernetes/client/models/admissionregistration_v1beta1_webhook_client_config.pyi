import datetime
import typing

import kubernetes.client

class AdmissionregistrationV1beta1WebhookClientConfig:
    ca_bundle: typing.Optional[str]
    service: typing.Optional[
        kubernetes.client.AdmissionregistrationV1beta1ServiceReference
    ]
    url: typing.Optional[str]
    def __init__(
        self,
        *,
        ca_bundle: typing.Optional[str] = ...,
        service: typing.Optional[
            kubernetes.client.AdmissionregistrationV1beta1ServiceReference
        ] = ...,
        url: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> AdmissionregistrationV1beta1WebhookClientConfigDict: ...

class AdmissionregistrationV1beta1WebhookClientConfigDict(
    typing.TypedDict, total=False
):
    caBundle: typing.Optional[str]
    service: typing.Optional[
        kubernetes.client.AdmissionregistrationV1beta1ServiceReferenceDict
    ]
    url: typing.Optional[str]
