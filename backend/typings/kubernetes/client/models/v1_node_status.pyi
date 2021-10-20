import datetime
import typing

import kubernetes.client

class V1NodeStatus:
    addresses: typing.Optional[list[kubernetes.client.V1NodeAddress]]
    allocatable: typing.Optional[dict[str, str]]
    capacity: typing.Optional[dict[str, str]]
    conditions: typing.Optional[list[kubernetes.client.V1NodeCondition]]
    config: typing.Optional[kubernetes.client.V1NodeConfigStatus]
    daemon_endpoints: typing.Optional[kubernetes.client.V1NodeDaemonEndpoints]
    images: typing.Optional[list[kubernetes.client.V1ContainerImage]]
    node_info: typing.Optional[kubernetes.client.V1NodeSystemInfo]
    phase: typing.Optional[str]
    volumes_attached: typing.Optional[list[kubernetes.client.V1AttachedVolume]]
    volumes_in_use: typing.Optional[list[str]]
    def __init__(
        self,
        *,
        addresses: typing.Optional[list[kubernetes.client.V1NodeAddress]] = ...,
        allocatable: typing.Optional[dict[str, str]] = ...,
        capacity: typing.Optional[dict[str, str]] = ...,
        conditions: typing.Optional[list[kubernetes.client.V1NodeCondition]] = ...,
        config: typing.Optional[kubernetes.client.V1NodeConfigStatus] = ...,
        daemon_endpoints: typing.Optional[
            kubernetes.client.V1NodeDaemonEndpoints
        ] = ...,
        images: typing.Optional[list[kubernetes.client.V1ContainerImage]] = ...,
        node_info: typing.Optional[kubernetes.client.V1NodeSystemInfo] = ...,
        phase: typing.Optional[str] = ...,
        volumes_attached: typing.Optional[
            list[kubernetes.client.V1AttachedVolume]
        ] = ...,
        volumes_in_use: typing.Optional[list[str]] = ...
    ) -> None: ...
    def to_dict(self) -> V1NodeStatusDict: ...

class V1NodeStatusDict(typing.TypedDict, total=False):
    addresses: typing.Optional[list[kubernetes.client.V1NodeAddressDict]]
    allocatable: typing.Optional[dict[str, str]]
    capacity: typing.Optional[dict[str, str]]
    conditions: typing.Optional[list[kubernetes.client.V1NodeConditionDict]]
    config: typing.Optional[kubernetes.client.V1NodeConfigStatusDict]
    daemonEndpoints: typing.Optional[kubernetes.client.V1NodeDaemonEndpointsDict]
    images: typing.Optional[list[kubernetes.client.V1ContainerImageDict]]
    nodeInfo: typing.Optional[kubernetes.client.V1NodeSystemInfoDict]
    phase: typing.Optional[str]
    volumesAttached: typing.Optional[list[kubernetes.client.V1AttachedVolumeDict]]
    volumesInUse: typing.Optional[list[str]]
