import datetime
import typing

import kubernetes.client

class V1ExternalDocumentation:
    description: typing.Optional[str]
    url: typing.Optional[str]
    def __init__(
        self,
        *,
        description: typing.Optional[str] = ...,
        url: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1ExternalDocumentationDict: ...

class V1ExternalDocumentationDict(typing.TypedDict, total=False):
    description: typing.Optional[str]
    url: typing.Optional[str]
