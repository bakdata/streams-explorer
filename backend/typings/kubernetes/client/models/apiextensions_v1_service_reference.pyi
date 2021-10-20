import datetime
import typing

import kubernetes.client

class ApiextensionsV1ServiceReference:
    name: str
    namespace: str
    path: typing.Optional[str]
    port: typing.Optional[int]
    def __init__(
        self,
        *,
        name: str,
        namespace: str,
        path: typing.Optional[str] = ...,
        port: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> ApiextensionsV1ServiceReferenceDict: ...

class ApiextensionsV1ServiceReferenceDict(typing.TypedDict, total=False):
    name: str
    namespace: str
    path: typing.Optional[str]
    port: typing.Optional[int]
