import datetime
import typing

import kubernetes.client

class V1alpha1UserSubject:
    name: str
    def __init__(self, *, name: str) -> None: ...
    def to_dict(self) -> V1alpha1UserSubjectDict: ...

class V1alpha1UserSubjectDict(typing.TypedDict, total=False):
    name: str
