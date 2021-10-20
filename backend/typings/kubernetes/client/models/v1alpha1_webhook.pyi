import datetime
import typing

import kubernetes.client

class V1alpha1Webhook:
    client_config: kubernetes.client.V1alpha1WebhookClientConfig
    throttle: typing.Optional[kubernetes.client.V1alpha1WebhookThrottleConfig]
    def __init__(
        self,
        *,
        client_config: kubernetes.client.V1alpha1WebhookClientConfig,
        throttle: typing.Optional[kubernetes.client.V1alpha1WebhookThrottleConfig] = ...
    ) -> None: ...
    def to_dict(self) -> V1alpha1WebhookDict: ...

class V1alpha1WebhookDict(typing.TypedDict, total=False):
    clientConfig: kubernetes.client.V1alpha1WebhookClientConfigDict
    throttle: typing.Optional[kubernetes.client.V1alpha1WebhookThrottleConfigDict]
