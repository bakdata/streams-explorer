import datetime
import typing

import kubernetes.client

class NetworkingV1beta1IngressTLS:
    hosts: typing.Optional[list[str]]
    secret_name: typing.Optional[str]
    def __init__(
        self,
        *,
        hosts: typing.Optional[list[str]] = ...,
        secret_name: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> NetworkingV1beta1IngressTLSDict: ...

class NetworkingV1beta1IngressTLSDict(typing.TypedDict, total=False):
    hosts: typing.Optional[list[str]]
    secretName: typing.Optional[str]
