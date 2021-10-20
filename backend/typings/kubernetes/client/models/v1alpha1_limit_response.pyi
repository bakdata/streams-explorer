import datetime
import typing

import kubernetes.client

class V1alpha1LimitResponse:
    queuing: typing.Optional[kubernetes.client.V1alpha1QueuingConfiguration]
    type: str
    def __init__(
        self,
        *,
        queuing: typing.Optional[kubernetes.client.V1alpha1QueuingConfiguration] = ...,
        type: str
    ) -> None: ...
    def to_dict(self) -> V1alpha1LimitResponseDict: ...

class V1alpha1LimitResponseDict(typing.TypedDict, total=False):
    queuing: typing.Optional[kubernetes.client.V1alpha1QueuingConfigurationDict]
    type: str
