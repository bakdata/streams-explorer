import typing

import kubernetes.client

class AuthorizationV1beta1Api:
    def __init__(
        self, api_client: typing.Optional[kubernetes.client.ApiClient] = ...
    ) -> None: ...
    def get_api_resources(self) -> kubernetes.client.V1APIResourceList: ...
    def create_namespaced_local_subject_access_review(
        self,
        namespace: str,
        body: kubernetes.client.V1beta1LocalSubjectAccessReview,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1beta1LocalSubjectAccessReview: ...
    def create_self_subject_access_review(
        self,
        body: kubernetes.client.V1beta1SelfSubjectAccessReview,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1beta1SelfSubjectAccessReview: ...
    def create_self_subject_rules_review(
        self,
        body: kubernetes.client.V1beta1SelfSubjectRulesReview,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1beta1SelfSubjectRulesReview: ...
    def create_subject_access_review(
        self,
        body: kubernetes.client.V1beta1SubjectAccessReview,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1beta1SubjectAccessReview: ...
