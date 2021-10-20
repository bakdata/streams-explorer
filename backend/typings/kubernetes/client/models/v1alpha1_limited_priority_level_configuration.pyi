import datetime
import typing

import kubernetes.client

class V1alpha1LimitedPriorityLevelConfiguration:
    assured_concurrency_shares: typing.Optional[int]
    limit_response: typing.Optional[kubernetes.client.V1alpha1LimitResponse]
    def __init__(
        self,
        *,
        assured_concurrency_shares: typing.Optional[int] = ...,
        limit_response: typing.Optional[kubernetes.client.V1alpha1LimitResponse] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1LimitedPriorityLevelConfigurationDict: ...

class V1alpha1LimitedPriorityLevelConfigurationDict(typing.TypedDict, total=False):
    assuredConcurrencyShares: typing.Optional[int]
    limitResponse: typing.Optional[kubernetes.client.V1alpha1LimitResponseDict]
