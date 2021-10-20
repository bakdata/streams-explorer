import datetime
import typing

import kubernetes.client

class V1MutatingWebhookConfiguration:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    webhooks: typing.Optional[list[kubernetes.client.V1MutatingWebhook]]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        webhooks: typing.Optional[list[kubernetes.client.V1MutatingWebhook]] = ...
    ) -> None: ...
    def to_dict(self) -> V1MutatingWebhookConfigurationDict: ...

class V1MutatingWebhookConfigurationDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    webhooks: typing.Optional[list[kubernetes.client.V1MutatingWebhookDict]]
