import datetime
import typing

import kubernetes.client

class V1EndpointAddress:
    hostname: typing.Optional[str]
    ip: str
    node_name: typing.Optional[str]
    target_ref: typing.Optional[kubernetes.client.V1ObjectReference]
    def __init__(
        self,
        *,
        hostname: typing.Optional[str] = ...,
        ip: str,
        node_name: typing.Optional[str] = ...,
        target_ref: typing.Optional[kubernetes.client.V1ObjectReference] = ...
    ) -> None: ...
    def to_dict(self) -> V1EndpointAddressDict: ...

class V1EndpointAddressDict(typing.TypedDict, total=False):
    hostname: typing.Optional[str]
    ip: str
    nodeName: typing.Optional[str]
    targetRef: typing.Optional[kubernetes.client.V1ObjectReferenceDict]
