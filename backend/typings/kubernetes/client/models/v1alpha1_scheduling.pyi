import datetime
import typing

import kubernetes.client

class V1alpha1Scheduling:
    node_selector: typing.Optional[dict[str, str]]
    tolerations: typing.Optional[list[kubernetes.client.V1Toleration]]
    def __init__(
        self,
        *,
        node_selector: typing.Optional[dict[str, str]] = ...,
        tolerations: typing.Optional[list[kubernetes.client.V1Toleration]] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1SchedulingDict: ...

class V1alpha1SchedulingDict(typing.TypedDict, total=False):
    nodeSelector: typing.Optional[dict[str, str]]
    tolerations: typing.Optional[list[kubernetes.client.V1TolerationDict]]
