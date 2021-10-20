import datetime
import typing

import kubernetes.client

class V1alpha1PriorityLevelConfigurationStatus:
    conditions: typing.Optional[
        list[kubernetes.client.V1alpha1PriorityLevelConfigurationCondition]
    ]
    def __init__(
        self,
        *,
        conditions: typing.Optional[
            list[kubernetes.client.V1alpha1PriorityLevelConfigurationCondition]
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1PriorityLevelConfigurationStatusDict: ...

class V1alpha1PriorityLevelConfigurationStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[
        list[kubernetes.client.V1alpha1PriorityLevelConfigurationConditionDict]
    ]
