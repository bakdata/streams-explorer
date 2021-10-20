import datetime
import typing

import kubernetes.client

class V1JobSpec:
    active_deadline_seconds: typing.Optional[int]
    backoff_limit: typing.Optional[int]
    completions: typing.Optional[int]
    manual_selector: typing.Optional[bool]
    parallelism: typing.Optional[int]
    selector: typing.Optional[kubernetes.client.V1LabelSelector]
    template: kubernetes.client.V1PodTemplateSpec
    ttl_seconds_after_finished: typing.Optional[int]
    def __init__(
        self,
        *,
        active_deadline_seconds: typing.Optional[int] = ...,
        backoff_limit: typing.Optional[int] = ...,
        completions: typing.Optional[int] = ...,
        manual_selector: typing.Optional[bool] = ...,
        parallelism: typing.Optional[int] = ...,
        selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...,
        template: kubernetes.client.V1PodTemplateSpec,
        ttl_seconds_after_finished: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1JobSpecDict: ...

class V1JobSpecDict(typing.TypedDict, total=False):
    activeDeadlineSeconds: typing.Optional[int]
    backoffLimit: typing.Optional[int]
    completions: typing.Optional[int]
    manualSelector: typing.Optional[bool]
    parallelism: typing.Optional[int]
    selector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    template: kubernetes.client.V1PodTemplateSpecDict
    ttlSecondsAfterFinished: typing.Optional[int]
