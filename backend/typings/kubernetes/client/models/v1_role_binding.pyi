import datetime
import typing

import kubernetes.client

class V1RoleBinding:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    role_ref: kubernetes.client.V1RoleRef
    subjects: typing.Optional[list[kubernetes.client.V1Subject]]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        role_ref: kubernetes.client.V1RoleRef,
        subjects: typing.Optional[list[kubernetes.client.V1Subject]] = ...
    ) -> None: ...
    def to_dict(self) -> V1RoleBindingDict: ...

class V1RoleBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    roleRef: kubernetes.client.V1RoleRefDict
    subjects: typing.Optional[list[kubernetes.client.V1SubjectDict]]
