import datetime
import typing

import kubernetes.client

class V1WindowsSecurityContextOptions:
    gmsa_credential_spec: typing.Optional[str]
    gmsa_credential_spec_name: typing.Optional[str]
    run_as_user_name: typing.Optional[str]
    def __init__(
        self,
        *,
        gmsa_credential_spec: typing.Optional[str] = ...,
        gmsa_credential_spec_name: typing.Optional[str] = ...,
        run_as_user_name: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1WindowsSecurityContextOptionsDict: ...

class V1WindowsSecurityContextOptionsDict(typing.TypedDict, total=False):
    gmsaCredentialSpec: typing.Optional[str]
    gmsaCredentialSpecName: typing.Optional[str]
    runAsUserName: typing.Optional[str]
