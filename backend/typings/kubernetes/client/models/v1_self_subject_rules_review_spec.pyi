import datetime
import typing

import kubernetes.client

class V1SelfSubjectRulesReviewSpec:
    namespace: typing.Optional[str]
    def __init__(self, *, namespace: typing.Optional[str] = ...) -> None: ...
    def to_dict(self) -> V1SelfSubjectRulesReviewSpecDict: ...

class V1SelfSubjectRulesReviewSpecDict(typing.TypedDict, total=False):
    namespace: typing.Optional[str]
