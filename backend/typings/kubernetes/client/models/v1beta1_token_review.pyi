import datetime
import typing

import kubernetes.client

class V1beta1TokenReview:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1TokenReviewSpec
    status: typing.Optional[kubernetes.client.V1beta1TokenReviewStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: kubernetes.client.V1beta1TokenReviewSpec,
        status: typing.Optional[kubernetes.client.V1beta1TokenReviewStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1TokenReviewDict: ...

class V1beta1TokenReviewDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1TokenReviewSpecDict
    status: typing.Optional[kubernetes.client.V1beta1TokenReviewStatusDict]
