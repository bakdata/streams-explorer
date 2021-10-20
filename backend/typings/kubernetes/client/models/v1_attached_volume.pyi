import datetime
import typing

import kubernetes.client

class V1AttachedVolume:
    device_path: str
    name: str
    def __init__(self, *, device_path: str, name: str) -> None: ...
    def to_dict(self) -> V1AttachedVolumeDict: ...

class V1AttachedVolumeDict(typing.TypedDict, total=False):
    devicePath: str
    name: str
