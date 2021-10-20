import datetime
import typing

import kubernetes.client

class V1beta1RunAsGroupStrategyOptions:
    ranges: typing.Optional[list[kubernetes.client.V1beta1IDRange]]
    rule: str
    def __init__(
        self,
        *,
        ranges: typing.Optional[list[kubernetes.client.V1beta1IDRange]] = ...,
        rule: str
    ) -> None: ...
    def to_dict(self) -> V1beta1RunAsGroupStrategyOptionsDict: ...

class V1beta1RunAsGroupStrategyOptionsDict(typing.TypedDict, total=False):
    ranges: typing.Optional[list[kubernetes.client.V1beta1IDRangeDict]]
    rule: str
