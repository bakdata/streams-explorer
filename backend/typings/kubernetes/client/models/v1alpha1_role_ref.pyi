import datetime
import typing

import kubernetes.client

class V1alpha1RoleRef:
    api_group: str
    kind: str
    name: str
    def __init__(self, *, api_group: str, kind: str, name: str) -> None: ...
    def to_dict(self) -> V1alpha1RoleRefDict: ...

class V1alpha1RoleRefDict(typing.TypedDict, total=False):
    apiGroup: str
    kind: str
    name: str
