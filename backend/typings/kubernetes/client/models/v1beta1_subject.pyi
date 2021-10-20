import datetime
import typing

import kubernetes.client

class V1beta1Subject:
    api_group: typing.Optional[str]
    kind: str
    name: str
    namespace: typing.Optional[str]
    def __init__(
        self,
        *,
        api_group: typing.Optional[str] = ...,
        kind: str,
        name: str,
        namespace: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1SubjectDict: ...

class V1beta1SubjectDict(typing.TypedDict, total=False):
    apiGroup: typing.Optional[str]
    kind: str
    name: str
    namespace: typing.Optional[str]
