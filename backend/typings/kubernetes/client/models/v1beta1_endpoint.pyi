import datetime
import typing

import kubernetes.client

class V1beta1Endpoint:
    addresses: list[str]
    conditions: typing.Optional[kubernetes.client.V1beta1EndpointConditions]
    hostname: typing.Optional[str]
    target_ref: typing.Optional[kubernetes.client.V1ObjectReference]
    topology: typing.Optional[dict[str, str]]
    def __init__(
        self,
        *,
        addresses: list[str],
        conditions: typing.Optional[kubernetes.client.V1beta1EndpointConditions] = ...,
        hostname: typing.Optional[str] = ...,
        target_ref: typing.Optional[kubernetes.client.V1ObjectReference] = ...,
        topology: typing.Optional[dict[str, str]] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1EndpointDict: ...

class V1beta1EndpointDict(typing.TypedDict, total=False):
    addresses: list[str]
    conditions: typing.Optional[kubernetes.client.V1beta1EndpointConditionsDict]
    hostname: typing.Optional[str]
    targetRef: typing.Optional[kubernetes.client.V1ObjectReferenceDict]
    topology: typing.Optional[dict[str, str]]
