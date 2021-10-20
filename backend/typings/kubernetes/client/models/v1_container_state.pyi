import datetime
import typing

import kubernetes.client

class V1ContainerState:
    running: typing.Optional[kubernetes.client.V1ContainerStateRunning]
    terminated: typing.Optional[kubernetes.client.V1ContainerStateTerminated]
    waiting: typing.Optional[kubernetes.client.V1ContainerStateWaiting]
    def __init__(
        self,
        *,
        running: typing.Optional[kubernetes.client.V1ContainerStateRunning] = ...,
        terminated: typing.Optional[kubernetes.client.V1ContainerStateTerminated] = ...,
        waiting: typing.Optional[kubernetes.client.V1ContainerStateWaiting] = ...
    ) -> None: ...
    def to_dict(self) -> V1ContainerStateDict: ...

class V1ContainerStateDict(typing.TypedDict, total=False):
    running: typing.Optional[kubernetes.client.V1ContainerStateRunningDict]
    terminated: typing.Optional[kubernetes.client.V1ContainerStateTerminatedDict]
    waiting: typing.Optional[kubernetes.client.V1ContainerStateWaitingDict]
