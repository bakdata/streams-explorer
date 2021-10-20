import datetime
import typing

import kubernetes.client

class V1Lifecycle:
    post_start: typing.Optional[kubernetes.client.V1Handler]
    pre_stop: typing.Optional[kubernetes.client.V1Handler]
    def __init__(
        self,
        *,
        post_start: typing.Optional[kubernetes.client.V1Handler] = ...,
        pre_stop: typing.Optional[kubernetes.client.V1Handler] = ...
    ) -> None: ...
    def to_dict(self) -> V1LifecycleDict: ...

class V1LifecycleDict(typing.TypedDict, total=False):
    postStart: typing.Optional[kubernetes.client.V1HandlerDict]
    preStop: typing.Optional[kubernetes.client.V1HandlerDict]
