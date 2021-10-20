import datetime
import typing

import kubernetes.client

class V1alpha1PriorityLevelConfigurationSpec:
    limited: typing.Optional[
        kubernetes.client.V1alpha1LimitedPriorityLevelConfiguration
    ]
    type: str
    def __init__(
        self,
        *,
        limited: typing.Optional[
            kubernetes.client.V1alpha1LimitedPriorityLevelConfiguration
        ] = ...,
        type: str
    ) -> None: ...
    def to_dict(self) -> V1alpha1PriorityLevelConfigurationSpecDict: ...

class V1alpha1PriorityLevelConfigurationSpecDict(typing.TypedDict, total=False):
    limited: typing.Optional[
        kubernetes.client.V1alpha1LimitedPriorityLevelConfigurationDict
    ]
    type: str
