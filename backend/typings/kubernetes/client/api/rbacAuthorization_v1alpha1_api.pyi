import typing

import kubernetes.client

class RbacAuthorizationV1alpha1Api:
    def __init__(
        self, api_client: typing.Optional[kubernetes.client.ApiClient] = ...
    ) -> None: ...
    def get_api_resources(self) -> kubernetes.client.V1APIResourceList: ...
    def list_cluster_role_binding(
        self,
        *,
        pretty: typing.Optional[str] = ...,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1ClusterRoleBindingList: ...
    def create_cluster_role_binding(
        self,
        body: kubernetes.client.V1alpha1ClusterRoleBinding,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1ClusterRoleBinding: ...
    def delete_collection_cluster_role_binding(
        self,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        _continue: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...
    ) -> kubernetes.client.V1Status: ...
    def read_cluster_role_binding(
        self, name: str, *, pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1ClusterRoleBinding: ...
    def replace_cluster_role_binding(
        self,
        name: str,
        body: kubernetes.client.V1alpha1ClusterRoleBinding,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1ClusterRoleBinding: ...
    def delete_cluster_role_binding(
        self,
        name: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        dry_run: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...
    ) -> kubernetes.client.V1Status: ...
    def patch_cluster_role_binding(
        self,
        name: str,
        body: typing.Any,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1ClusterRoleBinding: ...
    def list_cluster_role(
        self,
        *,
        pretty: typing.Optional[str] = ...,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1ClusterRoleList: ...
    def create_cluster_role(
        self,
        body: kubernetes.client.V1alpha1ClusterRole,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1ClusterRole: ...
    def delete_collection_cluster_role(
        self,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        _continue: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...
    ) -> kubernetes.client.V1Status: ...
    def read_cluster_role(
        self, name: str, *, pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1ClusterRole: ...
    def replace_cluster_role(
        self,
        name: str,
        body: kubernetes.client.V1alpha1ClusterRole,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1ClusterRole: ...
    def delete_cluster_role(
        self,
        name: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        dry_run: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...
    ) -> kubernetes.client.V1Status: ...
    def patch_cluster_role(
        self,
        name: str,
        body: typing.Any,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1ClusterRole: ...
    def list_namespaced_role_binding(
        self,
        namespace: str,
        *,
        pretty: typing.Optional[str] = ...,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1RoleBindingList: ...
    def create_namespaced_role_binding(
        self,
        namespace: str,
        body: kubernetes.client.V1alpha1RoleBinding,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1RoleBinding: ...
    def delete_collection_namespaced_role_binding(
        self,
        namespace: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        _continue: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...
    ) -> kubernetes.client.V1Status: ...
    def read_namespaced_role_binding(
        self, name: str, namespace: str, *, pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1RoleBinding: ...
    def replace_namespaced_role_binding(
        self,
        name: str,
        namespace: str,
        body: kubernetes.client.V1alpha1RoleBinding,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1RoleBinding: ...
    def delete_namespaced_role_binding(
        self,
        name: str,
        namespace: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        dry_run: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...
    ) -> kubernetes.client.V1Status: ...
    def patch_namespaced_role_binding(
        self,
        name: str,
        namespace: str,
        body: typing.Any,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1RoleBinding: ...
    def list_namespaced_role(
        self,
        namespace: str,
        *,
        pretty: typing.Optional[str] = ...,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1RoleList: ...
    def create_namespaced_role(
        self,
        namespace: str,
        body: kubernetes.client.V1alpha1Role,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1Role: ...
    def delete_collection_namespaced_role(
        self,
        namespace: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        _continue: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...
    ) -> kubernetes.client.V1Status: ...
    def read_namespaced_role(
        self, name: str, namespace: str, *, pretty: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1Role: ...
    def replace_namespaced_role(
        self,
        name: str,
        namespace: str,
        body: kubernetes.client.V1alpha1Role,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...
    ) -> kubernetes.client.V1alpha1Role: ...
    def delete_namespaced_role(
        self,
        name: str,
        namespace: str,
        *,
        pretty: typing.Optional[str] = ...,
        body: typing.Optional[kubernetes.client.V1DeleteOptions] = ...,
        dry_run: typing.Optional[str] = ...,
        grace_period_seconds: typing.Optional[int] = ...,
        orphan_dependents: typing.Optional[bool] = ...,
        propagation_policy: typing.Optional[str] = ...
    ) -> kubernetes.client.V1Status: ...
    def patch_namespaced_role(
        self,
        name: str,
        namespace: str,
        body: typing.Any,
        *,
        pretty: typing.Optional[str] = ...,
        dry_run: typing.Optional[str] = ...,
        field_manager: typing.Optional[str] = ...,
        force: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1Role: ...
    def list_role_binding_for_all_namespaces(
        self,
        *,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        pretty: typing.Optional[str] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1RoleBindingList: ...
    def list_role_for_all_namespaces(
        self,
        *,
        allow_watch_bookmarks: typing.Optional[bool] = ...,
        _continue: typing.Optional[str] = ...,
        field_selector: typing.Optional[str] = ...,
        label_selector: typing.Optional[str] = ...,
        limit: typing.Optional[int] = ...,
        pretty: typing.Optional[str] = ...,
        resource_version: typing.Optional[str] = ...,
        timeout_seconds: typing.Optional[int] = ...,
        watch: typing.Optional[bool] = ...
    ) -> kubernetes.client.V1alpha1RoleList: ...
