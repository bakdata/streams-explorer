import datetime
import typing

import kubernetes.client

class V1beta1EventSeries:
    count: int
    last_observed_time: datetime.datetime
    state: str
    def __init__(
        self, *, count: int, last_observed_time: datetime.datetime, state: str
    ) -> None: ...
    def to_dict(self) -> V1beta1EventSeriesDict: ...

class V1beta1EventSeriesDict(typing.TypedDict, total=False):
    count: int
    lastObservedTime: datetime.datetime
    state: str
