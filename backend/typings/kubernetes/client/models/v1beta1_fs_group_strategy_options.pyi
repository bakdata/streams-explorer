import datetime
import typing

import kubernetes.client

class V1beta1FSGroupStrategyOptions:
    ranges: typing.Optional[list[kubernetes.client.V1beta1IDRange]]
    rule: typing.Optional[str]
    def __init__(
        self,
        *,
        ranges: typing.Optional[list[kubernetes.client.V1beta1IDRange]] = ...,
        rule: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1FSGroupStrategyOptionsDict: ...

class V1beta1FSGroupStrategyOptionsDict(typing.TypedDict, total=False):
    ranges: typing.Optional[list[kubernetes.client.V1beta1IDRangeDict]]
    rule: typing.Optional[str]
