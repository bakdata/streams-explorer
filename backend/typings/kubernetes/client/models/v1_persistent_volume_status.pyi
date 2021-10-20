import datetime
import typing

import kubernetes.client

class V1PersistentVolumeStatus:
    message: typing.Optional[str]
    phase: typing.Optional[str]
    reason: typing.Optional[str]
    def __init__(
        self,
        *,
        message: typing.Optional[str] = ...,
        phase: typing.Optional[str] = ...,
        reason: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1PersistentVolumeStatusDict: ...

class V1PersistentVolumeStatusDict(typing.TypedDict, total=False):
    message: typing.Optional[str]
    phase: typing.Optional[str]
    reason: typing.Optional[str]
