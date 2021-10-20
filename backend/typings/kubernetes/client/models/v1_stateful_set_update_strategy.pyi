import datetime
import typing

import kubernetes.client

class V1StatefulSetUpdateStrategy:
    rolling_update: typing.Optional[
        kubernetes.client.V1RollingUpdateStatefulSetStrategy
    ]
    type: typing.Optional[str]
    def __init__(
        self,
        *,
        rolling_update: typing.Optional[
            kubernetes.client.V1RollingUpdateStatefulSetStrategy
        ] = ...,
        type: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1StatefulSetUpdateStrategyDict: ...

class V1StatefulSetUpdateStrategyDict(typing.TypedDict, total=False):
    rollingUpdate: typing.Optional[
        kubernetes.client.V1RollingUpdateStatefulSetStrategyDict
    ]
    type: typing.Optional[str]
