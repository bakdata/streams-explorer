import datetime
import typing

import kubernetes.client

class V1PodIP:
    ip: typing.Optional[str]
    def __init__(self, *, ip: typing.Optional[str] = ...) -> None: ...
    def to_dict(self) -> V1PodIPDict: ...

class V1PodIPDict(typing.TypedDict, total=False):
    ip: typing.Optional[str]
