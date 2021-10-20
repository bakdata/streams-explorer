import datetime
import typing

import kubernetes.client

class V1beta1ValidatingWebhookConfiguration:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    webhooks: typing.Optional[list[kubernetes.client.V1beta1ValidatingWebhook]]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        webhooks: typing.Optional[
            list[kubernetes.client.V1beta1ValidatingWebhook]
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1ValidatingWebhookConfigurationDict: ...

class V1beta1ValidatingWebhookConfigurationDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    webhooks: typing.Optional[list[kubernetes.client.V1beta1ValidatingWebhookDict]]
