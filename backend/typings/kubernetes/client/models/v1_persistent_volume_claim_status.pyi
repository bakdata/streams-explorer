import datetime
import typing

import kubernetes.client

class V1PersistentVolumeClaimStatus:
    access_modes: typing.Optional[list[str]]
    capacity: typing.Optional[dict[str, str]]
    conditions: typing.Optional[
        list[kubernetes.client.V1PersistentVolumeClaimCondition]
    ]
    phase: typing.Optional[str]
    def __init__(
        self,
        *,
        access_modes: typing.Optional[list[str]] = ...,
        capacity: typing.Optional[dict[str, str]] = ...,
        conditions: typing.Optional[
            list[kubernetes.client.V1PersistentVolumeClaimCondition]
        ] = ...,
        phase: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1PersistentVolumeClaimStatusDict: ...

class V1PersistentVolumeClaimStatusDict(typing.TypedDict, total=False):
    accessModes: typing.Optional[list[str]]
    capacity: typing.Optional[dict[str, str]]
    conditions: typing.Optional[
        list[kubernetes.client.V1PersistentVolumeClaimConditionDict]
    ]
    phase: typing.Optional[str]
