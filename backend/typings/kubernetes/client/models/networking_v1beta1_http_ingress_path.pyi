import datetime
import typing

import kubernetes.client

class NetworkingV1beta1HTTPIngressPath:
    backend: kubernetes.client.NetworkingV1beta1IngressBackend
    path: typing.Optional[str]
    path_type: typing.Optional[str]
    def __init__(
        self,
        *,
        backend: kubernetes.client.NetworkingV1beta1IngressBackend,
        path: typing.Optional[str] = ...,
        path_type: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> NetworkingV1beta1HTTPIngressPathDict: ...

class NetworkingV1beta1HTTPIngressPathDict(typing.TypedDict, total=False):
    backend: kubernetes.client.NetworkingV1beta1IngressBackendDict
    path: typing.Optional[str]
    pathType: typing.Optional[str]
