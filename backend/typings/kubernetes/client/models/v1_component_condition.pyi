import datetime
import typing

import kubernetes.client

class V1ComponentCondition:
    error: typing.Optional[str]
    message: typing.Optional[str]
    status: str
    type: str
    def __init__(
        self,
        *,
        error: typing.Optional[str] = ...,
        message: typing.Optional[str] = ...,
        status: str,
        type: str
    ) -> None: ...
    def to_dict(self) -> V1ComponentConditionDict: ...

class V1ComponentConditionDict(typing.TypedDict, total=False):
    error: typing.Optional[str]
    message: typing.Optional[str]
    status: str
    type: str
