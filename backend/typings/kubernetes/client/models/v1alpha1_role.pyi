import datetime
import typing

import kubernetes.client

class V1alpha1Role:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    rules: typing.Optional[list[kubernetes.client.V1alpha1PolicyRule]]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        rules: typing.Optional[list[kubernetes.client.V1alpha1PolicyRule]] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1RoleDict: ...

class V1alpha1RoleDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    rules: typing.Optional[list[kubernetes.client.V1alpha1PolicyRuleDict]]
