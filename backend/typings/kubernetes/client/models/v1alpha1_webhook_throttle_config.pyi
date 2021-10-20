import datetime
import typing

import kubernetes.client

class V1alpha1WebhookThrottleConfig:
    burst: typing.Optional[int]
    qps: typing.Optional[int]
    def __init__(
        self, *, burst: typing.Optional[int] = ..., qps: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1WebhookThrottleConfigDict: ...

class V1alpha1WebhookThrottleConfigDict(typing.TypedDict, total=False):
    burst: typing.Optional[int]
    qps: typing.Optional[int]
