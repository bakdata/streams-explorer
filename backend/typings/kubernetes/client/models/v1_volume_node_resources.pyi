import datetime
import typing

import kubernetes.client

class V1VolumeNodeResources:
    count: typing.Optional[int]
    def __init__(self, *, count: typing.Optional[int] = ...) -> None: ...
    def to_dict(self) -> V1VolumeNodeResourcesDict: ...

class V1VolumeNodeResourcesDict(typing.TypedDict, total=False):
    count: typing.Optional[int]
