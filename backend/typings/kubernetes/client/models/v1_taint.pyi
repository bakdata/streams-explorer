import datetime
import typing

import kubernetes.client

class V1Taint:
    effect: str
    key: str
    time_added: typing.Optional[datetime.datetime]
    value: typing.Optional[str]
    def __init__(
        self,
        *,
        effect: str,
        key: str,
        time_added: typing.Optional[datetime.datetime] = ...,
        value: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1TaintDict: ...

class V1TaintDict(typing.TypedDict, total=False):
    effect: str
    key: str
    timeAdded: typing.Optional[datetime.datetime]
    value: typing.Optional[str]
