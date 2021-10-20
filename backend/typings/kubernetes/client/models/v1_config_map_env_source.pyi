import datetime
import typing

import kubernetes.client

class V1ConfigMapEnvSource:
    name: typing.Optional[str]
    optional: typing.Optional[bool]
    def __init__(
        self, *, name: typing.Optional[str] = ..., optional: typing.Optional[bool] = ...
    ) -> None: ...
    def to_dict(self) -> V1ConfigMapEnvSourceDict: ...

class V1ConfigMapEnvSourceDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
    optional: typing.Optional[bool]
