import datetime
import typing

import kubernetes.client

class V1Event:
    action: typing.Optional[str]
    api_version: typing.Optional[str]
    count: typing.Optional[int]
    event_time: typing.Optional[datetime.datetime]
    first_timestamp: typing.Optional[datetime.datetime]
    involved_object: kubernetes.client.V1ObjectReference
    kind: typing.Optional[str]
    last_timestamp: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    metadata: kubernetes.client.V1ObjectMeta
    reason: typing.Optional[str]
    related: typing.Optional[kubernetes.client.V1ObjectReference]
    reporting_component: typing.Optional[str]
    reporting_instance: typing.Optional[str]
    series: typing.Optional[kubernetes.client.V1EventSeries]
    source: typing.Optional[kubernetes.client.V1EventSource]
    type: typing.Optional[str]
    def __init__(
        self,
        *,
        action: typing.Optional[str] = ...,
        api_version: typing.Optional[str] = ...,
        count: typing.Optional[int] = ...,
        event_time: typing.Optional[datetime.datetime] = ...,
        first_timestamp: typing.Optional[datetime.datetime] = ...,
        involved_object: kubernetes.client.V1ObjectReference,
        kind: typing.Optional[str] = ...,
        last_timestamp: typing.Optional[datetime.datetime] = ...,
        message: typing.Optional[str] = ...,
        metadata: kubernetes.client.V1ObjectMeta,
        reason: typing.Optional[str] = ...,
        related: typing.Optional[kubernetes.client.V1ObjectReference] = ...,
        reporting_component: typing.Optional[str] = ...,
        reporting_instance: typing.Optional[str] = ...,
        series: typing.Optional[kubernetes.client.V1EventSeries] = ...,
        source: typing.Optional[kubernetes.client.V1EventSource] = ...,
        type: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1EventDict: ...

class V1EventDict(typing.TypedDict, total=False):
    action: typing.Optional[str]
    apiVersion: typing.Optional[str]
    count: typing.Optional[int]
    eventTime: typing.Optional[datetime.datetime]
    firstTimestamp: typing.Optional[datetime.datetime]
    involvedObject: kubernetes.client.V1ObjectReferenceDict
    kind: typing.Optional[str]
    lastTimestamp: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    metadata: kubernetes.client.V1ObjectMetaDict
    reason: typing.Optional[str]
    related: typing.Optional[kubernetes.client.V1ObjectReferenceDict]
    reportingComponent: typing.Optional[str]
    reportingInstance: typing.Optional[str]
    series: typing.Optional[kubernetes.client.V1EventSeriesDict]
    source: typing.Optional[kubernetes.client.V1EventSourceDict]
    type: typing.Optional[str]
