import datetime
import typing

import kubernetes.client

class V1TokenRequestSpec:
    audiences: list[str]
    bound_object_ref: typing.Optional[kubernetes.client.V1BoundObjectReference]
    expiration_seconds: typing.Optional[int]
    def __init__(
        self,
        *,
        audiences: list[str],
        bound_object_ref: typing.Optional[
            kubernetes.client.V1BoundObjectReference
        ] = ...,
        expiration_seconds: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1TokenRequestSpecDict: ...

class V1TokenRequestSpecDict(typing.TypedDict, total=False):
    audiences: list[str]
    boundObjectRef: typing.Optional[kubernetes.client.V1BoundObjectReferenceDict]
    expirationSeconds: typing.Optional[int]
