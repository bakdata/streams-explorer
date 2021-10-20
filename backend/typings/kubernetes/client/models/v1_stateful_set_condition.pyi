import datetime
import typing

import kubernetes.client

class V1StatefulSetCondition:
    last_transition_time: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    reason: typing.Optional[str]
    status: str
    type: str
    def __init__(
        self,
        *,
        last_transition_time: typing.Optional[datetime.datetime] = ...,
        message: typing.Optional[str] = ...,
        reason: typing.Optional[str] = ...,
        status: str,
        type: str
    ) -> None: ...
    def to_dict(self) -> V1StatefulSetConditionDict: ...

class V1StatefulSetConditionDict(typing.TypedDict, total=False):
    lastTransitionTime: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    reason: typing.Optional[str]
    status: str
    type: str
