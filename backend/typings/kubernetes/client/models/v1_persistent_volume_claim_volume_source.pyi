import datetime
import typing

import kubernetes.client

class V1PersistentVolumeClaimVolumeSource:
    claim_name: str
    read_only: typing.Optional[bool]
    def __init__(
        self, *, claim_name: str, read_only: typing.Optional[bool] = ...
    ) -> None: ...
    def to_dict(self) -> V1PersistentVolumeClaimVolumeSourceDict: ...

class V1PersistentVolumeClaimVolumeSourceDict(typing.TypedDict, total=False):
    claimName: str
    readOnly: typing.Optional[bool]
