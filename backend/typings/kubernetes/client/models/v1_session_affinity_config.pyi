import datetime
import typing

import kubernetes.client

class V1SessionAffinityConfig:
    client_ip: typing.Optional[kubernetes.client.V1ClientIPConfig]
    def __init__(
        self, *, client_ip: typing.Optional[kubernetes.client.V1ClientIPConfig] = ...
    ) -> None: ...
    def to_dict(self) -> V1SessionAffinityConfigDict: ...

class V1SessionAffinityConfigDict(typing.TypedDict, total=False):
    clientIP: typing.Optional[kubernetes.client.V1ClientIPConfigDict]
