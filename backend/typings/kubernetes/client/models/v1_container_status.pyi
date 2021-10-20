import datetime
import typing

import kubernetes.client

class V1ContainerStatus:
    container_id: typing.Optional[str]
    image: str
    image_id: str
    last_state: typing.Optional[kubernetes.client.V1ContainerState]
    name: str
    ready: bool
    restart_count: int
    started: typing.Optional[bool]
    state: typing.Optional[kubernetes.client.V1ContainerState]
    def __init__(
        self,
        *,
        container_id: typing.Optional[str] = ...,
        image: str,
        image_id: str,
        last_state: typing.Optional[kubernetes.client.V1ContainerState] = ...,
        name: str,
        ready: bool,
        restart_count: int,
        started: typing.Optional[bool] = ...,
        state: typing.Optional[kubernetes.client.V1ContainerState] = ...
    ) -> None: ...
    def to_dict(self) -> V1ContainerStatusDict: ...

class V1ContainerStatusDict(typing.TypedDict, total=False):
    containerID: typing.Optional[str]
    image: str
    imageID: str
    lastState: typing.Optional[kubernetes.client.V1ContainerStateDict]
    name: str
    ready: bool
    restartCount: int
    started: typing.Optional[bool]
    state: typing.Optional[kubernetes.client.V1ContainerStateDict]
