import datetime
import typing

import kubernetes.client

class V1ScaleStatus:
    replicas: int
    selector: typing.Optional[str]
    def __init__(
        self, *, replicas: int, selector: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1ScaleStatusDict: ...

class V1ScaleStatusDict(typing.TypedDict, total=False):
    replicas: int
    selector: typing.Optional[str]
