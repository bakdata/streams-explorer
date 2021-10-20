import datetime
import typing

import kubernetes.client

class V1ConfigMapVolumeSource:
    default_mode: typing.Optional[int]
    items: typing.Optional[list[kubernetes.client.V1KeyToPath]]
    name: typing.Optional[str]
    optional: typing.Optional[bool]
    def __init__(
        self,
        *,
        default_mode: typing.Optional[int] = ...,
        items: typing.Optional[list[kubernetes.client.V1KeyToPath]] = ...,
        name: typing.Optional[str] = ...,
        optional: typing.Optional[bool] = ...
    ) -> None: ...
    def to_dict(self) -> V1ConfigMapVolumeSourceDict: ...

class V1ConfigMapVolumeSourceDict(typing.TypedDict, total=False):
    defaultMode: typing.Optional[int]
    items: typing.Optional[list[kubernetes.client.V1KeyToPathDict]]
    name: typing.Optional[str]
    optional: typing.Optional[bool]
