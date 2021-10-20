import datetime
import typing

import kubernetes.client

class V1TCPSocketAction:
    host: typing.Optional[str]
    port: typing.Any
    def __init__(
        self, *, host: typing.Optional[str] = ..., port: typing.Any
    ) -> None: ...
    def to_dict(self) -> V1TCPSocketActionDict: ...

class V1TCPSocketActionDict(typing.TypedDict, total=False):
    host: typing.Optional[str]
    port: typing.Any
