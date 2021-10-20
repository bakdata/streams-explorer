import datetime
import typing

import kubernetes.client

class V1ClusterRoleBindingList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1ClusterRoleBinding]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1ClusterRoleBinding],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1ClusterRoleBindingListDict: ...

class V1ClusterRoleBindingListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1ClusterRoleBindingDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
