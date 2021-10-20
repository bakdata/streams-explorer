import datetime
import typing

import kubernetes.client

class V1Handler:
    exec: typing.Optional[kubernetes.client.V1ExecAction]
    http_get: typing.Optional[kubernetes.client.V1HTTPGetAction]
    tcp_socket: typing.Optional[kubernetes.client.V1TCPSocketAction]
    def __init__(
        self,
        *,
        exec: typing.Optional[kubernetes.client.V1ExecAction] = ...,
        http_get: typing.Optional[kubernetes.client.V1HTTPGetAction] = ...,
        tcp_socket: typing.Optional[kubernetes.client.V1TCPSocketAction] = ...
    ) -> None: ...
    def to_dict(self) -> V1HandlerDict: ...

class V1HandlerDict(typing.TypedDict, total=False):
    exec: typing.Optional[kubernetes.client.V1ExecActionDict]
    httpGet: typing.Optional[kubernetes.client.V1HTTPGetActionDict]
    tcpSocket: typing.Optional[kubernetes.client.V1TCPSocketActionDict]
