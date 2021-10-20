import datetime
import typing

import kubernetes.client

class V1EphemeralContainer:
    args: typing.Optional[list[str]]
    command: typing.Optional[list[str]]
    env: typing.Optional[list[kubernetes.client.V1EnvVar]]
    env_from: typing.Optional[list[kubernetes.client.V1EnvFromSource]]
    image: typing.Optional[str]
    image_pull_policy: typing.Optional[str]
    lifecycle: typing.Optional[kubernetes.client.V1Lifecycle]
    liveness_probe: typing.Optional[kubernetes.client.V1Probe]
    name: str
    ports: typing.Optional[list[kubernetes.client.V1ContainerPort]]
    readiness_probe: typing.Optional[kubernetes.client.V1Probe]
    resources: typing.Optional[kubernetes.client.V1ResourceRequirements]
    security_context: typing.Optional[kubernetes.client.V1SecurityContext]
    startup_probe: typing.Optional[kubernetes.client.V1Probe]
    stdin: typing.Optional[bool]
    stdin_once: typing.Optional[bool]
    target_container_name: typing.Optional[str]
    termination_message_path: typing.Optional[str]
    termination_message_policy: typing.Optional[str]
    tty: typing.Optional[bool]
    volume_devices: typing.Optional[list[kubernetes.client.V1VolumeDevice]]
    volume_mounts: typing.Optional[list[kubernetes.client.V1VolumeMount]]
    working_dir: typing.Optional[str]
    def __init__(
        self,
        *,
        args: typing.Optional[list[str]] = ...,
        command: typing.Optional[list[str]] = ...,
        env: typing.Optional[list[kubernetes.client.V1EnvVar]] = ...,
        env_from: typing.Optional[list[kubernetes.client.V1EnvFromSource]] = ...,
        image: typing.Optional[str] = ...,
        image_pull_policy: typing.Optional[str] = ...,
        lifecycle: typing.Optional[kubernetes.client.V1Lifecycle] = ...,
        liveness_probe: typing.Optional[kubernetes.client.V1Probe] = ...,
        name: str,
        ports: typing.Optional[list[kubernetes.client.V1ContainerPort]] = ...,
        readiness_probe: typing.Optional[kubernetes.client.V1Probe] = ...,
        resources: typing.Optional[kubernetes.client.V1ResourceRequirements] = ...,
        security_context: typing.Optional[kubernetes.client.V1SecurityContext] = ...,
        startup_probe: typing.Optional[kubernetes.client.V1Probe] = ...,
        stdin: typing.Optional[bool] = ...,
        stdin_once: typing.Optional[bool] = ...,
        target_container_name: typing.Optional[str] = ...,
        termination_message_path: typing.Optional[str] = ...,
        termination_message_policy: typing.Optional[str] = ...,
        tty: typing.Optional[bool] = ...,
        volume_devices: typing.Optional[list[kubernetes.client.V1VolumeDevice]] = ...,
        volume_mounts: typing.Optional[list[kubernetes.client.V1VolumeMount]] = ...,
        working_dir: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1EphemeralContainerDict: ...

class V1EphemeralContainerDict(typing.TypedDict, total=False):
    args: typing.Optional[list[str]]
    command: typing.Optional[list[str]]
    env: typing.Optional[list[kubernetes.client.V1EnvVarDict]]
    envFrom: typing.Optional[list[kubernetes.client.V1EnvFromSourceDict]]
    image: typing.Optional[str]
    imagePullPolicy: typing.Optional[str]
    lifecycle: typing.Optional[kubernetes.client.V1LifecycleDict]
    livenessProbe: typing.Optional[kubernetes.client.V1ProbeDict]
    name: str
    ports: typing.Optional[list[kubernetes.client.V1ContainerPortDict]]
    readinessProbe: typing.Optional[kubernetes.client.V1ProbeDict]
    resources: typing.Optional[kubernetes.client.V1ResourceRequirementsDict]
    securityContext: typing.Optional[kubernetes.client.V1SecurityContextDict]
    startupProbe: typing.Optional[kubernetes.client.V1ProbeDict]
    stdin: typing.Optional[bool]
    stdinOnce: typing.Optional[bool]
    targetContainerName: typing.Optional[str]
    terminationMessagePath: typing.Optional[str]
    terminationMessagePolicy: typing.Optional[str]
    tty: typing.Optional[bool]
    volumeDevices: typing.Optional[list[kubernetes.client.V1VolumeDeviceDict]]
    volumeMounts: typing.Optional[list[kubernetes.client.V1VolumeMountDict]]
    workingDir: typing.Optional[str]
