import datetime
import typing

import kubernetes.client

class V1ServiceSpec:
    cluster_ip: typing.Optional[str]
    external_i_ps: typing.Optional[list[str]]
    external_name: typing.Optional[str]
    external_traffic_policy: typing.Optional[str]
    health_check_node_port: typing.Optional[int]
    ip_family: typing.Optional[str]
    load_balancer_ip: typing.Optional[str]
    load_balancer_source_ranges: typing.Optional[list[str]]
    ports: typing.Optional[list[kubernetes.client.V1ServicePort]]
    publish_not_ready_addresses: typing.Optional[bool]
    selector: typing.Optional[dict[str, str]]
    session_affinity: typing.Optional[str]
    session_affinity_config: typing.Optional[kubernetes.client.V1SessionAffinityConfig]
    topology_keys: typing.Optional[list[str]]
    type: typing.Optional[str]
    def __init__(
        self,
        *,
        cluster_ip: typing.Optional[str] = ...,
        external_i_ps: typing.Optional[list[str]] = ...,
        external_name: typing.Optional[str] = ...,
        external_traffic_policy: typing.Optional[str] = ...,
        health_check_node_port: typing.Optional[int] = ...,
        ip_family: typing.Optional[str] = ...,
        load_balancer_ip: typing.Optional[str] = ...,
        load_balancer_source_ranges: typing.Optional[list[str]] = ...,
        ports: typing.Optional[list[kubernetes.client.V1ServicePort]] = ...,
        publish_not_ready_addresses: typing.Optional[bool] = ...,
        selector: typing.Optional[dict[str, str]] = ...,
        session_affinity: typing.Optional[str] = ...,
        session_affinity_config: typing.Optional[
            kubernetes.client.V1SessionAffinityConfig
        ] = ...,
        topology_keys: typing.Optional[list[str]] = ...,
        type: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1ServiceSpecDict: ...

class V1ServiceSpecDict(typing.TypedDict, total=False):
    clusterIP: typing.Optional[str]
    externalIPs: typing.Optional[list[str]]
    externalName: typing.Optional[str]
    externalTrafficPolicy: typing.Optional[str]
    healthCheckNodePort: typing.Optional[int]
    ipFamily: typing.Optional[str]
    loadBalancerIP: typing.Optional[str]
    loadBalancerSourceRanges: typing.Optional[list[str]]
    ports: typing.Optional[list[kubernetes.client.V1ServicePortDict]]
    publishNotReadyAddresses: typing.Optional[bool]
    selector: typing.Optional[dict[str, str]]
    sessionAffinity: typing.Optional[str]
    sessionAffinityConfig: typing.Optional[
        kubernetes.client.V1SessionAffinityConfigDict
    ]
    topologyKeys: typing.Optional[list[str]]
    type: typing.Optional[str]
