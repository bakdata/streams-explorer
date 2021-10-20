import datetime
import typing

import kubernetes.client

class FlowcontrolV1alpha1Subject:
    group: typing.Optional[kubernetes.client.V1alpha1GroupSubject]
    kind: str
    service_account: typing.Optional[kubernetes.client.V1alpha1ServiceAccountSubject]
    user: typing.Optional[kubernetes.client.V1alpha1UserSubject]
    def __init__(
        self,
        *,
        group: typing.Optional[kubernetes.client.V1alpha1GroupSubject] = ...,
        kind: str,
        service_account: typing.Optional[
            kubernetes.client.V1alpha1ServiceAccountSubject
        ] = ...,
        user: typing.Optional[kubernetes.client.V1alpha1UserSubject] = ...
    ) -> None: ...
    def to_dict(self) -> FlowcontrolV1alpha1SubjectDict: ...

class FlowcontrolV1alpha1SubjectDict(typing.TypedDict, total=False):
    group: typing.Optional[kubernetes.client.V1alpha1GroupSubjectDict]
    kind: str
    serviceAccount: typing.Optional[kubernetes.client.V1alpha1ServiceAccountSubjectDict]
    user: typing.Optional[kubernetes.client.V1alpha1UserSubjectDict]
