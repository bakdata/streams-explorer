import datetime
import typing

import kubernetes.client

class V1NodeAddress:
    address: str
    type: str
    def __init__(self, *, address: str, type: str) -> None: ...
    def to_dict(self) -> V1NodeAddressDict: ...

class V1NodeAddressDict(typing.TypedDict, total=False):
    address: str
    type: str
