import datetime
import typing

import kubernetes.client

class V1alpha1WebhookClientConfig:
    ca_bundle: typing.Optional[str]
    service: typing.Optional[kubernetes.client.V1alpha1ServiceReference]
    url: typing.Optional[str]
    def __init__(
        self,
        *,
        ca_bundle: typing.Optional[str] = ...,
        service: typing.Optional[kubernetes.client.V1alpha1ServiceReference] = ...,
        url: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1WebhookClientConfigDict: ...

class V1alpha1WebhookClientConfigDict(typing.TypedDict, total=False):
    caBundle: typing.Optional[str]
    service: typing.Optional[kubernetes.client.V1alpha1ServiceReferenceDict]
    url: typing.Optional[str]
