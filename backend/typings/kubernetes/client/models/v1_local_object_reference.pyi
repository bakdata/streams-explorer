import datetime
import typing

import kubernetes.client

class V1LocalObjectReference:
    name: typing.Optional[str]
    def __init__(self, *, name: typing.Optional[str] = ...) -> None: ...
    def to_dict(self) -> V1LocalObjectReferenceDict: ...

class V1LocalObjectReferenceDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
