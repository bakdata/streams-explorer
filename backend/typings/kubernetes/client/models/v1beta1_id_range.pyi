import datetime
import typing

import kubernetes.client

class V1beta1IDRange:
    max: int
    min: int
    def __init__(self, *, max: int, min: int) -> None: ...
    def to_dict(self) -> V1beta1IDRangeDict: ...

class V1beta1IDRangeDict(typing.TypedDict, total=False):
    max: int
    min: int
