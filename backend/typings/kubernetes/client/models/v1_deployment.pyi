import datetime
import typing

import kubernetes.client

class V1Deployment:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1DeploymentSpec]
    status: typing.Optional[kubernetes.client.V1DeploymentStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1DeploymentSpec] = ...,
        status: typing.Optional[kubernetes.client.V1DeploymentStatus] = ...
    ) -> None: ...
    def to_dict(self) -> V1DeploymentDict: ...

class V1DeploymentDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1DeploymentSpecDict]
    status: typing.Optional[kubernetes.client.V1DeploymentStatusDict]
