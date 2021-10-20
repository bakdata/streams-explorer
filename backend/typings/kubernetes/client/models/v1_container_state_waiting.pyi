import datetime
import typing

import kubernetes.client

class V1ContainerStateWaiting:
    message: typing.Optional[str]
    reason: typing.Optional[str]
    def __init__(
        self, *, message: typing.Optional[str] = ..., reason: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1ContainerStateWaitingDict: ...

class V1ContainerStateWaitingDict(typing.TypedDict, total=False):
    message: typing.Optional[str]
    reason: typing.Optional[str]
