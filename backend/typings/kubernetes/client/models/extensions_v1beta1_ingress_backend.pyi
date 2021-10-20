import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1IngressBackend:
    resource: typing.Optional[kubernetes.client.V1TypedLocalObjectReference]
    service_name: typing.Optional[str]
    service_port: typing.Optional[typing.Any]
    def __init__(
        self,
        *,
        resource: typing.Optional[kubernetes.client.V1TypedLocalObjectReference] = ...,
        service_name: typing.Optional[str] = ...,
        service_port: typing.Optional[typing.Any] = ...
    ) -> None: ...
    def to_dict(self) -> ExtensionsV1beta1IngressBackendDict: ...

class ExtensionsV1beta1IngressBackendDict(typing.TypedDict, total=False):
    resource: typing.Optional[kubernetes.client.V1TypedLocalObjectReferenceDict]
    serviceName: typing.Optional[str]
    servicePort: typing.Optional[typing.Any]
