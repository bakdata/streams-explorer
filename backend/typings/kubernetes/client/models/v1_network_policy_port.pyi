import datetime
import typing

import kubernetes.client

class V1NetworkPolicyPort:
    port: typing.Optional[typing.Any]
    protocol: typing.Optional[str]
    def __init__(
        self,
        *,
        port: typing.Optional[typing.Any] = ...,
        protocol: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1NetworkPolicyPortDict: ...

class V1NetworkPolicyPortDict(typing.TypedDict, total=False):
    port: typing.Optional[typing.Any]
    protocol: typing.Optional[str]
