import datetime
import typing

import kubernetes.client

class V1ServiceAccountTokenProjection:
    audience: typing.Optional[str]
    expiration_seconds: typing.Optional[int]
    path: str
    def __init__(
        self,
        *,
        audience: typing.Optional[str] = ...,
        expiration_seconds: typing.Optional[int] = ...,
        path: str
    ) -> None: ...
    def to_dict(self) -> V1ServiceAccountTokenProjectionDict: ...

class V1ServiceAccountTokenProjectionDict(typing.TypedDict, total=False):
    audience: typing.Optional[str]
    expirationSeconds: typing.Optional[int]
    path: str
