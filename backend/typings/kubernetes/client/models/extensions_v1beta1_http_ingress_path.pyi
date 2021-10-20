import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1HTTPIngressPath:
    backend: kubernetes.client.ExtensionsV1beta1IngressBackend
    path: typing.Optional[str]
    path_type: typing.Optional[str]
    def __init__(
        self,
        *,
        backend: kubernetes.client.ExtensionsV1beta1IngressBackend,
        path: typing.Optional[str] = ...,
        path_type: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> ExtensionsV1beta1HTTPIngressPathDict: ...

class ExtensionsV1beta1HTTPIngressPathDict(typing.TypedDict, total=False):
    backend: kubernetes.client.ExtensionsV1beta1IngressBackendDict
    path: typing.Optional[str]
    pathType: typing.Optional[str]
