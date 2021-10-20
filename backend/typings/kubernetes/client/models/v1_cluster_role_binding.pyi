import datetime
import typing

import kubernetes.client

class V1ClusterRoleBinding:
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
    def to_dict(self) -> V1ClusterRoleBindingDict: ...

class V1ClusterRoleBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    roleRef: kubernetes.client.V1RoleRefDict
    subjects: typing.Optional[list[kubernetes.client.V1SubjectDict]]
