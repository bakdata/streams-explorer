import datetime
import typing

import kubernetes.client

class V1beta1EndpointPort:
    app_protocol: typing.Optional[str]
    name: typing.Optional[str]
    port: typing.Optional[int]
    protocol: typing.Optional[str]
    def __init__(
        self,
        *,
        app_protocol: typing.Optional[str] = ...,
        name: typing.Optional[str] = ...,
        port: typing.Optional[int] = ...,
        protocol: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1EndpointPortDict: ...

class V1beta1EndpointPortDict(typing.TypedDict, total=False):
    appProtocol: typing.Optional[str]
    name: typing.Optional[str]
    port: typing.Optional[int]
    protocol: typing.Optional[str]
