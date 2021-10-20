import datetime
import typing

import kubernetes.client

class V1beta1LeaseSpec:
    acquire_time: typing.Optional[datetime.datetime]
    holder_identity: typing.Optional[str]
    lease_duration_seconds: typing.Optional[int]
    lease_transitions: typing.Optional[int]
    renew_time: typing.Optional[datetime.datetime]
    def __init__(
        self,
        *,
        acquire_time: typing.Optional[datetime.datetime] = ...,
        holder_identity: typing.Optional[str] = ...,
        lease_duration_seconds: typing.Optional[int] = ...,
        lease_transitions: typing.Optional[int] = ...,
        renew_time: typing.Optional[datetime.datetime] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1LeaseSpecDict: ...

class V1beta1LeaseSpecDict(typing.TypedDict, total=False):
    acquireTime: typing.Optional[datetime.datetime]
    holderIdentity: typing.Optional[str]
    leaseDurationSeconds: typing.Optional[int]
    leaseTransitions: typing.Optional[int]
    renewTime: typing.Optional[datetime.datetime]
