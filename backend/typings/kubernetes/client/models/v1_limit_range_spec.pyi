import datetime
import typing

import kubernetes.client

class V1LimitRangeSpec:
    limits: list[kubernetes.client.V1LimitRangeItem]
    def __init__(self, *, limits: list[kubernetes.client.V1LimitRangeItem]) -> None: ...
    def to_dict(self) -> V1LimitRangeSpecDict: ...

class V1LimitRangeSpecDict(typing.TypedDict, total=False):
    limits: list[kubernetes.client.V1LimitRangeItemDict]
