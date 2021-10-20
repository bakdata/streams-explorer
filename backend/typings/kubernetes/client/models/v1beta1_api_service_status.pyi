import datetime
import typing

import kubernetes.client

class V1beta1APIServiceStatus:
    conditions: typing.Optional[list[kubernetes.client.V1beta1APIServiceCondition]]
    def __init__(
        self,
        *,
        conditions: typing.Optional[
            list[kubernetes.client.V1beta1APIServiceCondition]
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1APIServiceStatusDict: ...

class V1beta1APIServiceStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1beta1APIServiceConditionDict]]
