import datetime
import typing

import kubernetes.client

class V1ProjectedVolumeSource:
    default_mode: typing.Optional[int]
    sources: list[kubernetes.client.V1VolumeProjection]
    def __init__(
        self,
        *,
        default_mode: typing.Optional[int] = ...,
        sources: list[kubernetes.client.V1VolumeProjection]
    ) -> None: ...
    def to_dict(self) -> V1ProjectedVolumeSourceDict: ...

class V1ProjectedVolumeSourceDict(typing.TypedDict, total=False):
    defaultMode: typing.Optional[int]
    sources: list[kubernetes.client.V1VolumeProjectionDict]
