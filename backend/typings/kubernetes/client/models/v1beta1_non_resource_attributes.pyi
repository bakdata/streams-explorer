import datetime
import typing

import kubernetes.client

class V1beta1NonResourceAttributes:
    path: typing.Optional[str]
    verb: typing.Optional[str]
    def __init__(
        self, *, path: typing.Optional[str] = ..., verb: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1NonResourceAttributesDict: ...

class V1beta1NonResourceAttributesDict(typing.TypedDict, total=False):
    path: typing.Optional[str]
    verb: typing.Optional[str]
