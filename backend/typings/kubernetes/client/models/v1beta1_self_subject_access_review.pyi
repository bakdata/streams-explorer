import datetime
import typing

import kubernetes.client

class V1beta1SelfSubjectAccessReview:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1SelfSubjectAccessReviewSpec
    status: typing.Optional[kubernetes.client.V1beta1SubjectAccessReviewStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: kubernetes.client.V1beta1SelfSubjectAccessReviewSpec,
        status: typing.Optional[
            kubernetes.client.V1beta1SubjectAccessReviewStatus
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1SelfSubjectAccessReviewDict: ...

class V1beta1SelfSubjectAccessReviewDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1SelfSubjectAccessReviewSpecDict
    status: typing.Optional[kubernetes.client.V1beta1SubjectAccessReviewStatusDict]
