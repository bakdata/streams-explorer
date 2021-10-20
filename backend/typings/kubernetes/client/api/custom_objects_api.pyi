import typing

import kubernetes.client

class CustomObjectsApi:
    def __init__(
        self, api_client: typing.Optional[kubernetes.client.ApiClient] = ...
    ) -> None: ...
    def list_namespaced_custom_object(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        *,
        pretty: typing.Optional[str] = ...,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        resource_version: typing.Optional[str] = ...,
        resource_version_match: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> typing.Any: ...
    def create_namespaced_custom_object(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        body: typing.Any,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> None: ...
    def delete_collection_namespaced_custom_object(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def list_cluster_custom_object(
        self,
        group: str,
        version: str,
        plural: str,
        *,
        pretty: typing.Optional[str] = ...,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        resource_version: typing.Optional[str] = ...,
        resource_version_match: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> typing.Any: ...
    def create_cluster_custom_object(
        self,
        group: str,
        version: str,
        plural: str,
        body: typing.Any,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> None: ...
    def delete_collection_cluster_custom_object(
        self,
        group: str,
        version: str,
        plural: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def get_cluster_custom_object_status(
        self, group: str, version: str, plural: str, name: str
    ) -> typing.Any: ...
    def replace_cluster_custom_object_status(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def patch_cluster_custom_object_status(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> typing.Any: ...
    def get_namespaced_custom_object(
        self, group: str, version: str, namespace: str, plural: str, name: str
    ) -> typing.Any: ...
    def replace_namespaced_custom_object(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def delete_namespaced_custom_object(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        name: str,
        *,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def patch_namespaced_custom_object(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> typing.Any: ...
    def get_namespaced_custom_object_scale(
        self, group: str, version: str, namespace: str, plural: str, name: str
    ) -> typing.Any: ...
    def replace_namespaced_custom_object_scale(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def patch_namespaced_custom_object_scale(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> typing.Any: ...
    def get_cluster_custom_object_scale(
        self, group: str, version: str, plural: str, name: str
    ) -> typing.Any: ...
    def replace_cluster_custom_object_scale(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def patch_cluster_custom_object_scale(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> typing.Any: ...
    def get_cluster_custom_object(
        self, group: str, version: str, plural: str, name: str
    ) -> typing.Any: ...
    def replace_cluster_custom_object(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def delete_cluster_custom_object(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        *,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def patch_cluster_custom_object(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> typing.Any: ...
    def get_namespaced_custom_object_status(
        self, group: str, version: str, namespace: str, plural: str, name: str
    ) -> typing.Any: ...
    def replace_namespaced_custom_object_status(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> typing.Any: ...
    def patch_namespaced_custom_object_status(
        self,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        name: str,
        body: typing.Any,
        *,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> typing.Any: ...
