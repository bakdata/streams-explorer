import datetime
import typing

import kubernetes.client

class V2alpha1CronJob:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V2alpha1CronJobSpec]
    status: typing.Optional[kubernetes.client.V2alpha1CronJobStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V2alpha1CronJobSpec] = ...,
        status: typing.Optional[kubernetes.client.V2alpha1CronJobStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V2alpha1CronJobDict: ...

class V2alpha1CronJobDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V2alpha1CronJobSpecDict]
    status: typing.Optional[kubernetes.client.V2alpha1CronJobStatusDict]
