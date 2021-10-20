import datetime
import typing

import kubernetes.client

class V1beta1UserInfo:
    extra: typing.Optional[dict[str, list[str]]]
    groups: typing.Optional[list[str]]
    uid: typing.Optional[str]
    username: typing.Optional[str]
    def __init__(
        self,
        *,
        extra: typing.Optional[dict[str, list[str]]] = ...,
        groups: typing.Optional[list[str]] = ...,
        uid: typing.Optional[str] = ...,
        username: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1UserInfoDict: ...

class V1beta1UserInfoDict(typing.TypedDict, total=False):
    extra: typing.Optional[dict[str, list[str]]]
    groups: typing.Optional[list[str]]
    uid: typing.Optional[str]
    username: typing.Optional[str]
