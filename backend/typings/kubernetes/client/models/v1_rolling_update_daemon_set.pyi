import datetime
import typing

import kubernetes.client

class V1RollingUpdateDaemonSet:
    max_unavailable: typing.Optional[typing.Any]
    def __init__(
        self, *, max_unavailable: typing.Optional[typing.Any] = ...
    ) -> None: ...
    def to_dict(self) -> V1RollingUpdateDaemonSetDict: ...

class V1RollingUpdateDaemonSetDict(typing.TypedDict, total=False):
    maxUnavailable: typing.Optional[typing.Any]
