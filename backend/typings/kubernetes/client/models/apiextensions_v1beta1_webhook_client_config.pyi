import datetime
import typing

import kubernetes.client

class ApiextensionsV1beta1WebhookClientConfig:
    ca_bundle: typing.Optional[str]
    service: typing.Optional[kubernetes.client.ApiextensionsV1beta1ServiceReference]
    url: typing.Optional[str]
    def __init__(
        self,
        *,
        ca_bundle: typing.Optional[str] = ...,
        service: typing.Optional[
            kubernetes.client.ApiextensionsV1beta1ServiceReference
        ] = ...,
        url: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> ApiextensionsV1beta1WebhookClientConfigDict: ...

class ApiextensionsV1beta1WebhookClientConfigDict(typing.TypedDict, total=False):
    caBundle: typing.Optional[str]
    service: typing.Optional[kubernetes.client.ApiextensionsV1beta1ServiceReferenceDict]
    url: typing.Optional[str]
