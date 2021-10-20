import datetime
import typing

import kubernetes.client

class V1DownwardAPIVolumeSource:
    default_mode: typing.Optional[int]
    items: typing.Optional[list[kubernetes.client.V1DownwardAPIVolumeFile]]
    def __init__(
        self,
        *,
        default_mode: typing.Optional[int] = ...,
        items: typing.Optional[list[kubernetes.client.V1DownwardAPIVolumeFile]] = ...
    ) -> None: ...
    def to_dict(self) -> V1DownwardAPIVolumeSourceDict: ...

class V1DownwardAPIVolumeSourceDict(typing.TypedDict, total=False):
    defaultMode: typing.Optional[int]
    items: typing.Optional[list[kubernetes.client.V1DownwardAPIVolumeFileDict]]
