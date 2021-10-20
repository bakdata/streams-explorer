import datetime
import typing

import kubernetes.client

class V1ResourceRequirements:
    limits: typing.Optional[dict[str, str]]
    requests: typing.Optional[dict[str, str]]
    def __init__(
        self,
        *,
        limits: typing.Optional[dict[str, str]] = ...,
        requests: typing.Optional[dict[str, str]] = ...
    ) -> None: ...
    def to_dict(self) -> V1ResourceRequirementsDict: ...

class V1ResourceRequirementsDict(typing.TypedDict, total=False):
    limits: typing.Optional[dict[str, str]]
    requests: typing.Optional[dict[str, str]]
