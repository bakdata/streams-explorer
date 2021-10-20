import datetime
import typing

import kubernetes.client

class V1EnvVarSource:
    config_map_key_ref: typing.Optional[kubernetes.client.V1ConfigMapKeySelector]
    field_ref: typing.Optional[kubernetes.client.V1ObjectFieldSelector]
    resource_field_ref: typing.Optional[kubernetes.client.V1ResourceFieldSelector]
    secret_key_ref: typing.Optional[kubernetes.client.V1SecretKeySelector]
    def __init__(
        self,
        *,
        config_map_key_ref: typing.Optional[
            kubernetes.client.V1ConfigMapKeySelector
        ] = ...,
        field_ref: typing.Optional[kubernetes.client.V1ObjectFieldSelector] = ...,
        resource_field_ref: typing.Optional[
            kubernetes.client.V1ResourceFieldSelector
        ] = ...,
        secret_key_ref: typing.Optional[kubernetes.client.V1SecretKeySelector] = ...
    ) -> None: ...
    def to_dict(self) -> V1EnvVarSourceDict: ...

class V1EnvVarSourceDict(typing.TypedDict, total=False):
    configMapKeyRef: typing.Optional[kubernetes.client.V1ConfigMapKeySelectorDict]
    fieldRef: typing.Optional[kubernetes.client.V1ObjectFieldSelectorDict]
    resourceFieldRef: typing.Optional[kubernetes.client.V1ResourceFieldSelectorDict]
    secretKeyRef: typing.Optional[kubernetes.client.V1SecretKeySelectorDict]
