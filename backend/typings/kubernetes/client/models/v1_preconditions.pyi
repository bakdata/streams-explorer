import datetime
import typing

import kubernetes.client

class V1Preconditions:
    resource_version: typing.Optional[str]
    uid: typing.Optional[str]
    def __init__(
        self,
        *,
        resource_version: typing.Optional[str] = ...,
        uid: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1PreconditionsDict: ...

class V1PreconditionsDict(typing.TypedDict, total=False):
    resourceVersion: typing.Optional[str]
    uid: typing.Optional[str]
