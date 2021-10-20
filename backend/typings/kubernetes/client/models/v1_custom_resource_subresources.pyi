import datetime
import typing

import kubernetes.client

class V1CustomResourceSubresources:
    scale: typing.Optional[kubernetes.client.V1CustomResourceSubresourceScale]
    status: typing.Optional[typing.Any]
    def __init__(
        self,
        *,
        scale: typing.Optional[
            kubernetes.client.V1CustomResourceSubresourceScale
        ] = ...,
        status: typing.Optional[typing.Any] = ...
    ) -> None: ...
    def to_dict(self) -> V1CustomResourceSubresourcesDict: ...

class V1CustomResourceSubresourcesDict(typing.TypedDict, total=False):
    scale: typing.Optional[kubernetes.client.V1CustomResourceSubresourceScaleDict]
    status: typing.Optional[typing.Any]
