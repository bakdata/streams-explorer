import datetime
import typing

import kubernetes.client

class V1alpha1AuditSinkSpec:
    policy: kubernetes.client.V1alpha1Policy
    webhook: kubernetes.client.V1alpha1Webhook
    def __init__(
        self,
        *,
        policy: kubernetes.client.V1alpha1Policy,
        webhook: kubernetes.client.V1alpha1Webhook
    ) -> None: ...
    def to_dict(self) -> V1alpha1AuditSinkSpecDict: ...

class V1alpha1AuditSinkSpecDict(typing.TypedDict, total=False):
    policy: kubernetes.client.V1alpha1PolicyDict
    webhook: kubernetes.client.V1alpha1WebhookDict
