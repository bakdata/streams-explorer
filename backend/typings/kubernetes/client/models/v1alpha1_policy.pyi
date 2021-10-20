import datetime
import typing

import kubernetes.client

class V1alpha1Policy:
    level: str
    stages: typing.Optional[list[str]]
    def __init__(
        self, *, level: str, stages: typing.Optional[list[str]] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1PolicyDict: ...

class V1alpha1PolicyDict(typing.TypedDict, total=False):
    level: str
    stages: typing.Optional[list[str]]
