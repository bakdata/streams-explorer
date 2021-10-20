import datetime
import typing

import kubernetes.client

class V1alpha1RuntimeClassSpec:
    overhead: typing.Optional[kubernetes.client.V1alpha1Overhead]
    runtime_handler: str
    scheduling: typing.Optional[kubernetes.client.V1alpha1Scheduling]
    def __init__(
        self,
        *,
        overhead: typing.Optional[kubernetes.client.V1alpha1Overhead] = ...,
        runtime_handler: str,
        scheduling: typing.Optional[kubernetes.client.V1alpha1Scheduling] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1RuntimeClassSpecDict: ...

class V1alpha1RuntimeClassSpecDict(typing.TypedDict, total=False):
    overhead: typing.Optional[kubernetes.client.V1alpha1OverheadDict]
    runtimeHandler: str
    scheduling: typing.Optional[kubernetes.client.V1alpha1SchedulingDict]
