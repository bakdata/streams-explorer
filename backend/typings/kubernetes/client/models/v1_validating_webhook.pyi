import datetime
import typing

import kubernetes.client

class V1ValidatingWebhook:
    admission_review_versions: list[str]
    client_config: kubernetes.client.AdmissionregistrationV1WebhookClientConfig
    failure_policy: typing.Optional[str]
    match_policy: typing.Optional[str]
    name: str
    namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    object_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    rules: typing.Optional[list[kubernetes.client.V1RuleWithOperations]]
    side_effects: str
    timeout_seconds: typing.Optional[int]
    def __init__(
        self,
        *,
        admission_review_versions: list[str],
        client_config: kubernetes.client.AdmissionregistrationV1WebhookClientConfig,
        failure_policy: typing.Optional[str] = ...,
        match_policy: typing.Optional[str] = ...,
        name: str,
        namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...,
        object_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...,
        rules: typing.Optional[list[kubernetes.client.V1RuleWithOperations]] = ...,
        side_effects: str,
        timeout_seconds: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1ValidatingWebhookDict: ...

class V1ValidatingWebhookDict(typing.TypedDict, total=False):
    admissionReviewVersions: list[str]
    clientConfig: kubernetes.client.AdmissionregistrationV1WebhookClientConfigDict
    failurePolicy: typing.Optional[str]
    matchPolicy: typing.Optional[str]
    name: str
    namespaceSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    objectSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    rules: typing.Optional[list[kubernetes.client.V1RuleWithOperationsDict]]
    sideEffects: str
    timeoutSeconds: typing.Optional[int]
