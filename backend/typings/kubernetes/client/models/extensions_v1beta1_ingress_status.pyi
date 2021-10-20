import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1IngressStatus:
    load_balancer: typing.Optional[kubernetes.client.V1LoadBalancerStatus]
    def __init__(
        self,
        *,
        load_balancer: typing.Optional[kubernetes.client.V1LoadBalancerStatus] = ...
    ) -> None: ...
    def to_dict(self) -> ExtensionsV1beta1IngressStatusDict: ...

class ExtensionsV1beta1IngressStatusDict(typing.TypedDict, total=False):
    loadBalancer: typing.Optional[kubernetes.client.V1LoadBalancerStatusDict]
