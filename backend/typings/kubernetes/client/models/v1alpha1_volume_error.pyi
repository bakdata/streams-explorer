import datetime
import typing

import kubernetes.client

class V1alpha1VolumeError:
    message: typing.Optional[str]
    time: typing.Optional[datetime.datetime]
    def __init__(
        self,
        *,
        message: typing.Optional[str] = ...,
        time: typing.Optional[datetime.datetime] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1VolumeErrorDict: ...

class V1alpha1VolumeErrorDict(typing.TypedDict, total=False):
    message: typing.Optional[str]
    time: typing.Optional[datetime.datetime]
