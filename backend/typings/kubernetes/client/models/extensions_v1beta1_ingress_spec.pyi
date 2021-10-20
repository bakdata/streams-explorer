import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1IngressSpec:
    backend: typing.Optional[kubernetes.client.ExtensionsV1beta1IngressBackend]
    ingress_class_name: typing.Optional[str]
    rules: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IngressRule]]
    tls: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IngressTLS]]
    def __init__(
        self,
        *,
        backend: typing.Optional[
            kubernetes.client.ExtensionsV1beta1IngressBackend
        ] = ...,
        ingress_class_name: typing.Optional[str] = ...,
        rules: typing.Optional[
            list[kubernetes.client.ExtensionsV1beta1IngressRule]
        ] = ...,
        tls: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IngressTLS]] = ...
    ) -> None: ...
    def to_dict(self) -> ExtensionsV1beta1IngressSpecDict: ...

class ExtensionsV1beta1IngressSpecDict(typing.TypedDict, total=False):
    backend: typing.Optional[kubernetes.client.ExtensionsV1beta1IngressBackendDict]
    ingressClassName: typing.Optional[str]
    rules: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IngressRuleDict]]
    tls: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IngressTLSDict]]
