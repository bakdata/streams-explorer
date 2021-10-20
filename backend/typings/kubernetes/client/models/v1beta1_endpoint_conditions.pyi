import datetime
import typing

import kubernetes.client

class V1beta1EndpointConditions:
    ready: typing.Optional[bool]
    def __init__(self, *, ready: typing.Optional[bool] = ...) -> None: ...
    def to_dict(self) -> V1beta1EndpointConditionsDict: ...

class V1beta1EndpointConditionsDict(typing.TypedDict, total=False):
    ready: typing.Optional[bool]
