import datetime
import typing

import kubernetes.client

class V1PodSecurityContext:
    fs_group: typing.Optional[int]
    fs_group_change_policy: typing.Optional[str]
    run_as_group: typing.Optional[int]
    run_as_non_root: typing.Optional[bool]
    run_as_user: typing.Optional[int]
    se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions]
    supplemental_groups: typing.Optional[list[int]]
    sysctls: typing.Optional[list[kubernetes.client.V1Sysctl]]
    windows_options: typing.Optional[kubernetes.client.V1WindowsSecurityContextOptions]
    def __init__(
        self,
        *,
        fs_group: typing.Optional[int] = ...,
        fs_group_change_policy: typing.Optional[str] = ...,
        run_as_group: typing.Optional[int] = ...,
        run_as_non_root: typing.Optional[bool] = ...,
        run_as_user: typing.Optional[int] = ...,
        se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions] = ...,
        supplemental_groups: typing.Optional[list[int]] = ...,
        sysctls: typing.Optional[list[kubernetes.client.V1Sysctl]] = ...,
        windows_options: typing.Optional[
            kubernetes.client.V1WindowsSecurityContextOptions
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1PodSecurityContextDict: ...

class V1PodSecurityContextDict(typing.TypedDict, total=False):
    fsGroup: typing.Optional[int]
    fsGroupChangePolicy: typing.Optional[str]
    runAsGroup: typing.Optional[int]
    runAsNonRoot: typing.Optional[bool]
    runAsUser: typing.Optional[int]
    seLinuxOptions: typing.Optional[kubernetes.client.V1SELinuxOptionsDict]
    supplementalGroups: typing.Optional[list[int]]
    sysctls: typing.Optional[list[kubernetes.client.V1SysctlDict]]
    windowsOptions: typing.Optional[
        kubernetes.client.V1WindowsSecurityContextOptionsDict
    ]
