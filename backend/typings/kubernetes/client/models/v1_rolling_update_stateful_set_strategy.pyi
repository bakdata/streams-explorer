import datetime
import typing

import kubernetes.client

class V1RollingUpdateStatefulSetStrategy:
    partition: typing.Optional[int]
    def __init__(self, *, partition: typing.Optional[int] = ...) -> None: ...
    def to_dict(self) -> V1RollingUpdateStatefulSetStrategyDict: ...

class V1RollingUpdateStatefulSetStrategyDict(typing.TypedDict, total=False):
    partition: typing.Optional[int]
