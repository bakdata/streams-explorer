import datetime
import typing

import kubernetes.client

class V1FlockerVolumeSource:
    dataset_name: typing.Optional[str]
    dataset_uuid: typing.Optional[str]
    def __init__(
        self,
        *,
        dataset_name: typing.Optional[str] = ...,
        dataset_uuid: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1FlockerVolumeSourceDict: ...

class V1FlockerVolumeSourceDict(typing.TypedDict, total=False):
    datasetName: typing.Optional[str]
    datasetUUID: typing.Optional[str]
