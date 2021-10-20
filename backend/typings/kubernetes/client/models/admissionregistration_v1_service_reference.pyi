import datetime
import typing

import kubernetes.client

class AdmissionregistrationV1ServiceReference:
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
    def to_dict(self) -> AdmissionregistrationV1ServiceReferenceDict: ...

class AdmissionregistrationV1ServiceReferenceDict(typing.TypedDict, total=False):
    name: str
    namespace: str
    path: typing.Optional[str]
    port: typing.Optional[int]
