import datetime
import typing

import kubernetes.client

class V1alpha1NonResourcePolicyRule:
    non_resource_ur_ls: list[str]
    verbs: list[str]
    def __init__(self, *, non_resource_ur_ls: list[str], verbs: list[str]) -> None: ...
    def to_dict(self) -> V1alpha1NonResourcePolicyRuleDict: ...

class V1alpha1NonResourcePolicyRuleDict(typing.TypedDict, total=False):
    nonResourceURLs: list[str]
    verbs: list[str]
