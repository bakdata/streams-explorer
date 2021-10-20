import datetime
import typing

import kubernetes.client

class V1ClientIPConfig:
    timeout_seconds: typing.Optional[int]
    def __init__(self, *, timeout_seconds: typing.Optional[int] = ...) -> None: ...
    def to_dict(self) -> V1ClientIPConfigDict: ...

class V1ClientIPConfigDict(typing.TypedDict, total=False):
    timeoutSeconds: typing.Optional[int]
