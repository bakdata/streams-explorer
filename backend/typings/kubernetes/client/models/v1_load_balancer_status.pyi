import datetime
import typing

import kubernetes.client

class V1LoadBalancerStatus:
    ingress: typing.Optional[list[kubernetes.client.V1LoadBalancerIngress]]
    def __init__(
        self,
        *,
        ingress: typing.Optional[list[kubernetes.client.V1LoadBalancerIngress]] = ...
    ) -> None: ...
    def to_dict(self) -> V1LoadBalancerStatusDict: ...

class V1LoadBalancerStatusDict(typing.TypedDict, total=False):
    ingress: typing.Optional[list[kubernetes.client.V1LoadBalancerIngressDict]]
