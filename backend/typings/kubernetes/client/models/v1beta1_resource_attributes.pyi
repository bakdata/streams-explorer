import datetime
import typing

import kubernetes.client

class V1beta1ResourceAttributes:
    group: typing.Optional[str]
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    resource: typing.Optional[str]
    subresource: typing.Optional[str]
    verb: typing.Optional[str]
    version: typing.Optional[str]
    def __init__(
        self,
        *,
        group: typing.Optional[str] = ...,
        name: typing.Optional[str] = ...,
        namespace: typing.Optional[str] = ...,
        resource: typing.Optional[str] = ...,
        subresource: typing.Optional[str] = ...,
        verb: typing.Optional[str] = ...,
        version: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1ResourceAttributesDict: ...

class V1beta1ResourceAttributesDict(typing.TypedDict, total=False):
    group: typing.Optional[str]
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    resource: typing.Optional[str]
    subresource: typing.Optional[str]
    verb: typing.Optional[str]
    version: typing.Optional[str]
