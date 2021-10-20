import datetime
import typing

import kubernetes.client

class V1NetworkPolicyIngressRule:
    _from: typing.Optional[list[kubernetes.client.V1NetworkPolicyPeer]]
    ports: typing.Optional[list[kubernetes.client.V1NetworkPolicyPort]]
    def __init__(
        self,
        *,
        _from: typing.Optional[list[kubernetes.client.V1NetworkPolicyPeer]] = ...,
        ports: typing.Optional[list[kubernetes.client.V1NetworkPolicyPort]] = ...
    ) -> None: ...
    def to_dict(self) -> V1NetworkPolicyIngressRuleDict: ...

class V1NetworkPolicyIngressRuleDict(typing.TypedDict, total=False):
    _from: typing.Optional[list[kubernetes.client.V1NetworkPolicyPeerDict]]
    ports: typing.Optional[list[kubernetes.client.V1NetworkPolicyPortDict]]
