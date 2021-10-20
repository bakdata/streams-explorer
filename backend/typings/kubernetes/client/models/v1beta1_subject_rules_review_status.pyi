import datetime
import typing

import kubernetes.client

class V1beta1SubjectRulesReviewStatus:
    evaluation_error: typing.Optional[str]
    incomplete: bool
    non_resource_rules: list[kubernetes.client.V1beta1NonResourceRule]
    resource_rules: list[kubernetes.client.V1beta1ResourceRule]
    def __init__(
        self,
        *,
        evaluation_error: typing.Optional[str] = ...,
        incomplete: bool,
        non_resource_rules: list[kubernetes.client.V1beta1NonResourceRule],
        resource_rules: list[kubernetes.client.V1beta1ResourceRule]
    ) -> None: ...
    def to_dict(self) -> V1beta1SubjectRulesReviewStatusDict: ...

class V1beta1SubjectRulesReviewStatusDict(typing.TypedDict, total=False):
    evaluationError: typing.Optional[str]
    incomplete: bool
    nonResourceRules: list[kubernetes.client.V1beta1NonResourceRuleDict]
    resourceRules: list[kubernetes.client.V1beta1ResourceRuleDict]
