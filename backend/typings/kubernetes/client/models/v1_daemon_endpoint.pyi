import datetime
import typing

import kubernetes.client

class V1DaemonEndpoint:
    port: int
    def __init__(self, *, port: int) -> None: ...
    def to_dict(self) -> V1DaemonEndpointDict: ...

class V1DaemonEndpointDict(typing.TypedDict, total=False):
    Port: int
