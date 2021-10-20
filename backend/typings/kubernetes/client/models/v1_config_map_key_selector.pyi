import datetime
import typing

import kubernetes.client

class V1ConfigMapKeySelector:
    key: str
    name: typing.Optional[str]
    optional: typing.Optional[bool]
    def __init__(
        self,
        *,
        key: str,
        name: typing.Optional[str] = ...,
        optional: typing.Optional[bool] = ...
    ) -> None: ...
    def to_dict(self) -> V1ConfigMapKeySelectorDict: ...

class V1ConfigMapKeySelectorDict(typing.TypedDict, total=False):
    key: str
    name: typing.Optional[str]
    optional: typing.Optional[bool]
