import datetime
import typing

import kubernetes.client

class V1alpha1RoleBinding:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    role_ref: kubernetes.client.V1alpha1RoleRef
    subjects: typing.Optional[list[kubernetes.client.RbacV1alpha1Subject]]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        role_ref: kubernetes.client.V1alpha1RoleRef,
        subjects: typing.Optional[list[kubernetes.client.RbacV1alpha1Subject]] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1RoleBindingDict: ...

class V1alpha1RoleBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    roleRef: kubernetes.client.V1alpha1RoleRefDict
    subjects: typing.Optional[list[kubernetes.client.RbacV1alpha1SubjectDict]]
