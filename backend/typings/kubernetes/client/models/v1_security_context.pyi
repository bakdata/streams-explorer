import datetime
import typing

import kubernetes.client

class V1SecurityContext:
    allow_privilege_escalation: typing.Optional[bool]
    capabilities: typing.Optional[kubernetes.client.V1Capabilities]
    privileged: typing.Optional[bool]
    proc_mount: typing.Optional[str]
    read_only_root_filesystem: typing.Optional[bool]
    run_as_group: typing.Optional[int]
    run_as_non_root: typing.Optional[bool]
    run_as_user: typing.Optional[int]
    se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions]
    windows_options: typing.Optional[kubernetes.client.V1WindowsSecurityContextOptions]
    def __init__(
        self,
        *,
        allow_privilege_escalation: typing.Optional[bool] = ...,
        capabilities: typing.Optional[kubernetes.client.V1Capabilities] = ...,
        privileged: typing.Optional[bool] = ...,
        proc_mount: typing.Optional[str] = ...,
        read_only_root_filesystem: typing.Optional[bool] = ...,
        run_as_group: typing.Optional[int] = ...,
        run_as_non_root: typing.Optional[bool] = ...,
        run_as_user: typing.Optional[int] = ...,
        se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions] = ...,
        windows_options: typing.Optional[
            kubernetes.client.V1WindowsSecurityContextOptions
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1SecurityContextDict: ...

class V1SecurityContextDict(typing.TypedDict, total=False):
    allowPrivilegeEscalation: typing.Optional[bool]
    capabilities: typing.Optional[kubernetes.client.V1CapabilitiesDict]
    privileged: typing.Optional[bool]
    procMount: typing.Optional[str]
    readOnlyRootFilesystem: typing.Optional[bool]
    runAsGroup: typing.Optional[int]
    runAsNonRoot: typing.Optional[bool]
    runAsUser: typing.Optional[int]
    seLinuxOptions: typing.Optional[kubernetes.client.V1SELinuxOptionsDict]
    windowsOptions: typing.Optional[
        kubernetes.client.V1WindowsSecurityContextOptionsDict
    ]
