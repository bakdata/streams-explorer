import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1IngressRule:
    host: typing.Optional[str]
    http: typing.Optional[kubernetes.client.ExtensionsV1beta1HTTPIngressRuleValue]
    def __init__(
        self,
        *,
        host: typing.Optional[str] = ...,
        http: typing.Optional[
            kubernetes.client.ExtensionsV1beta1HTTPIngressRuleValue
        ] = ...
    ) -> None: ...
    def to_dict(self) -> ExtensionsV1beta1IngressRuleDict: ...

class ExtensionsV1beta1IngressRuleDict(typing.TypedDict, total=False):
    host: typing.Optional[str]
    http: typing.Optional[kubernetes.client.ExtensionsV1beta1HTTPIngressRuleValueDict]
