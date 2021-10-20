import datetime
import typing

import kubernetes.client

class V1TokenRequestStatus:
    expiration_timestamp: datetime.datetime
    token: str
    def __init__(
        self, *, expiration_timestamp: datetime.datetime, token: str
    ) -> None: ...
    def to_dict(self) -> V1TokenRequestStatusDict: ...

class V1TokenRequestStatusDict(typing.TypedDict, total=False):
    expirationTimestamp: datetime.datetime
    token: str
