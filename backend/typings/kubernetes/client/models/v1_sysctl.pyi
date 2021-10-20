import datetime
import typing

import kubernetes.client

class V1Sysctl:
    name: str
    value: str
    def __init__(self, *, name: str, value: str) -> None: ...
    def to_dict(self) -> V1SysctlDict: ...

class V1SysctlDict(typing.TypedDict, total=False):
    name: str
    value: str
