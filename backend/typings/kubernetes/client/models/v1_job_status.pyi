import datetime
import typing

import kubernetes.client

class V1JobStatus:
    active: typing.Optional[int]
    completion_time: typing.Optional[datetime.datetime]
    conditions: typing.Optional[list[kubernetes.client.V1JobCondition]]
    failed: typing.Optional[int]
    start_time: typing.Optional[datetime.datetime]
    succeeded: typing.Optional[int]
    def __init__(
        self,
        *,
        active: typing.Optional[int] = ...,
        completion_time: typing.Optional[datetime.datetime] = ...,
        conditions: typing.Optional[list[kubernetes.client.V1JobCondition]] = ...,
        failed: typing.Optional[int] = ...,
        start_time: typing.Optional[datetime.datetime] = ...,
        succeeded: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1JobStatusDict: ...

class V1JobStatusDict(typing.TypedDict, total=False):
    active: typing.Optional[int]
    completionTime: typing.Optional[datetime.datetime]
    conditions: typing.Optional[list[kubernetes.client.V1JobConditionDict]]
    failed: typing.Optional[int]
    startTime: typing.Optional[datetime.datetime]
    succeeded: typing.Optional[int]
