import datetime
import typing

import kubernetes.client

class V1beta1ExternalDocumentation:
    description: typing.Optional[str]
    url: typing.Optional[str]
    def __init__(
        self,
        *,
        description: typing.Optional[str] = ...,
        url: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1ExternalDocumentationDict: ...

class V1beta1ExternalDocumentationDict(typing.TypedDict, total=False):
    description: typing.Optional[str]
    url: typing.Optional[str]
