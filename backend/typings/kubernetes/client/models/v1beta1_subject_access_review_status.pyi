import datetime
import typing

import kubernetes.client

class V1beta1SubjectAccessReviewStatus:
    allowed: bool
    denied: typing.Optional[bool]
    evaluation_error: typing.Optional[str]
    reason: typing.Optional[str]
    def __init__(
        self,
        *,
        allowed: bool,
        denied: typing.Optional[bool] = ...,
        evaluation_error: typing.Optional[str] = ...,
        reason: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1SubjectAccessReviewStatusDict: ...

class V1beta1SubjectAccessReviewStatusDict(typing.TypedDict, total=False):
    allowed: bool
    denied: typing.Optional[bool]
    evaluationError: typing.Optional[str]
    reason: typing.Optional[str]
