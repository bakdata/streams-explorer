import datetime
import typing

import kubernetes.client

class V1GitRepoVolumeSource:
    directory: typing.Optional[str]
    repository: str
    revision: typing.Optional[str]
    def __init__(
        self,
        *,
        directory: typing.Optional[str] = ...,
        repository: str,
        revision: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1GitRepoVolumeSourceDict: ...

class V1GitRepoVolumeSourceDict(typing.TypedDict, total=False):
    directory: typing.Optional[str]
    repository: str
    revision: typing.Optional[str]
