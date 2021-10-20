import datetime
import typing

import kubernetes.client

class V1beta1ClusterRoleBinding:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    role_ref: kubernetes.client.V1beta1RoleRef
    subjects: typing.Optional[list[kubernetes.client.V1beta1Subject]]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        role_ref: kubernetes.client.V1beta1RoleRef,
        subjects: typing.Optional[list[kubernetes.client.V1beta1Subject]] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1ClusterRoleBindingDict: ...

class V1beta1ClusterRoleBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    roleRef: kubernetes.client.V1beta1RoleRefDict
    subjects: typing.Optional[list[kubernetes.client.V1beta1SubjectDict]]
