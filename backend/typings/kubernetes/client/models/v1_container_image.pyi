import datetime
import typing

import kubernetes.client

class V1ContainerImage:
    names: list[str]
    size_bytes: typing.Optional[int]
    def __init__(
        self, *, names: list[str], size_bytes: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1ContainerImageDict: ...

class V1ContainerImageDict(typing.TypedDict, total=False):
    names: list[str]
    sizeBytes: typing.Optional[int]
