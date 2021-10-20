import datetime
import typing

import kubernetes.client

class V1beta1ValidatingWebhook:
    admission_review_versions: typing.Optional[list[str]]
    client_config: kubernetes.client.AdmissionregistrationV1beta1WebhookClientConfig
    failure_policy: typing.Optional[str]
    match_policy: typing.Optional[str]
    name: str
    namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    object_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    rules: typing.Optional[list[kubernetes.client.V1beta1RuleWithOperations]]
    side_effects: typing.Optional[str]
    timeout_seconds: typing.Optional[int]
    def __init__(
        self,
        *,
        admission_review_versions: typing.Optional[list[str]] = ...,
        client_config: kubernetes.client.AdmissionregistrationV1beta1WebhookClientConfig,
        failure_policy: typing.Optional[str] = ...,
        match_policy: typing.Optional[str] = ...,
        name: str,
        namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...,
        object_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...,
        rules: typing.Optional[list[kubernetes.client.V1beta1RuleWithOperations]] = ...,
        side_effects: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1ValidatingWebhookDict: ...

class V1beta1ValidatingWebhookDict(typing.TypedDict, total=False):
    admissionReviewVersions: typing.Optional[list[str]]
    clientConfig: kubernetes.client.AdmissionregistrationV1beta1WebhookClientConfigDict
    failurePolicy: typing.Optional[str]
    matchPolicy: typing.Optional[str]
    name: str
    namespaceSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    objectSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    rules: typing.Optional[list[kubernetes.client.V1beta1RuleWithOperationsDict]]
    sideEffects: typing.Optional[str]
    timeoutSeconds: typing.Optional[int]
