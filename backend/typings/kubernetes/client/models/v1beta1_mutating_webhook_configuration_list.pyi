import datetime
import typing

import kubernetes.client

class V1beta1MutatingWebhookConfigurationList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1beta1MutatingWebhookConfiguration]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1beta1MutatingWebhookConfiguration],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1MutatingWebhookConfigurationListDict: ...

class V1beta1MutatingWebhookConfigurationListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1beta1MutatingWebhookConfigurationDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
