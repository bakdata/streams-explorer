import datetime
import typing

import kubernetes.client

class V1ValidatingWebhookConfigurationList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1ValidatingWebhookConfiguration]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        items: list[kubernetes.client.V1ValidatingWebhookConfiguration],
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...
    ) -> None: ...
    def to_dict(self) -> V1ValidatingWebhookConfigurationListDict: ...

class V1ValidatingWebhookConfigurationListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1ValidatingWebhookConfigurationDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
