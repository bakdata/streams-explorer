import datetime
import typing

import kubernetes.client

class V1beta1AllowedCSIDriver:
    name: str
    def __init__(self, *, name: str) -> None: ...
    def to_dict(self) -> V1beta1AllowedCSIDriverDict: ...

class V1beta1AllowedCSIDriverDict(typing.TypedDict, total=False):
    name: str
