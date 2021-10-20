import datetime
import typing

import kubernetes.client

class V1ScaleSpec:
    replicas: typing.Optional[int]
    def __init__(self, *, replicas: typing.Optional[int] = ...) -> None: ...
    def to_dict(self) -> V1ScaleSpecDict: ...

class V1ScaleSpecDict(typing.TypedDict, total=False):
    replicas: typing.Optional[int]
