import datetime
import typing

import kubernetes.client

class V1HTTPHeader:
    name: str
    value: str
    def __init__(self, *, name: str, value: str) -> None: ...
    def to_dict(self) -> V1HTTPHeaderDict: ...

class V1HTTPHeaderDict(typing.TypedDict, total=False):
    name: str
    value: str
