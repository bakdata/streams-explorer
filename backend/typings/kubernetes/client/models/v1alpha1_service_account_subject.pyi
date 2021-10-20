import datetime
import typing

import kubernetes.client

class V1alpha1ServiceAccountSubject:
    name: str
    namespace: str
    def __init__(self, *, name: str, namespace: str) -> None: ...
    def to_dict(self) -> V1alpha1ServiceAccountSubjectDict: ...

class V1alpha1ServiceAccountSubjectDict(typing.TypedDict, total=False):
    name: str
    namespace: str
