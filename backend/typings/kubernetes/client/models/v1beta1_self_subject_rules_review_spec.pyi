import datetime
import typing

import kubernetes.client

class V1beta1SelfSubjectRulesReviewSpec:
    namespace: typing.Optional[str]
    def __init__(self, *, namespace: typing.Optional[str] = ...) -> None: ...
    def to_dict(self) -> V1beta1SelfSubjectRulesReviewSpecDict: ...

class V1beta1SelfSubjectRulesReviewSpecDict(typing.TypedDict, total=False):
    namespace: typing.Optional[str]
