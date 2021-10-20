import datetime
import typing

import kubernetes.client

class V1TypedLocalObjectReference:
    api_group: typing.Optional[str]
    kind: str
    name: str
    def __init__(
        self, *, api_group: typing.Optional[str] = ..., kind: str, name: str
    ) -> None: ...
    def to_dict(self) -> V1TypedLocalObjectReferenceDict: ...

class V1TypedLocalObjectReferenceDict(typing.TypedDict, total=False):
    apiGroup: typing.Optional[str]
    kind: str
    name: str
