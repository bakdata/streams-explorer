import datetime
import typing

import kubernetes.client

class AdmissionregistrationV1WebhookClientConfig:
    ca_bundle: typing.Optional[str]
    service: typing.Optional[kubernetes.client.AdmissionregistrationV1ServiceReference]
    url: typing.Optional[str]
    def __init__(
        self,
        *,
        ca_bundle: typing.Optional[str] = ...,
        service: typing.Optional[
            kubernetes.client.AdmissionregistrationV1ServiceReference
        ] = ...,
        url: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> AdmissionregistrationV1WebhookClientConfigDict: ...

class AdmissionregistrationV1WebhookClientConfigDict(typing.TypedDict, total=False):
    caBundle: typing.Optional[str]
    service: typing.Optional[
        kubernetes.client.AdmissionregistrationV1ServiceReferenceDict
    ]
    url: typing.Optional[str]
