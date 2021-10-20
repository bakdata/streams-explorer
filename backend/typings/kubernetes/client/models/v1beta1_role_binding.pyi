import datetime
import typing

import kubernetes.client

class V1beta1RoleBinding:
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
    def to_dict(self) -> V1beta1RoleBindingDict: ...

class V1beta1RoleBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    roleRef: kubernetes.client.V1beta1RoleRefDict
    subjects: typing.Optional[list[kubernetes.client.V1beta1SubjectDict]]
