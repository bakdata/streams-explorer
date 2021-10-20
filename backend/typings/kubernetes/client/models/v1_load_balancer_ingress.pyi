import datetime
import typing

import kubernetes.client

class V1LoadBalancerIngress:
    hostname: typing.Optional[str]
    ip: typing.Optional[str]
    def __init__(
        self, *, hostname: typing.Optional[str] = ..., ip: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1LoadBalancerIngressDict: ...

class V1LoadBalancerIngressDict(typing.TypedDict, total=False):
    hostname: typing.Optional[str]
    ip: typing.Optional[str]
