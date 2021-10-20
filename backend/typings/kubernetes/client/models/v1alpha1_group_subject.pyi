import datetime
import typing

import kubernetes.client

class V1alpha1GroupSubject:
    name: str
    def __init__(self, *, name: str) -> None: ...
    def to_dict(self) -> V1alpha1GroupSubjectDict: ...

class V1alpha1GroupSubjectDict(typing.TypedDict, total=False):
    name: str
