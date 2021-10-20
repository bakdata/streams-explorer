import datetime
import typing

import kubernetes.client

class V1SelfSubjectAccessReviewSpec:
    non_resource_attributes: typing.Optional[kubernetes.client.V1NonResourceAttributes]
    resource_attributes: typing.Optional[kubernetes.client.V1ResourceAttributes]
    def __init__(
        self,
        *,
        non_resource_attributes: typing.Optional[
            kubernetes.client.V1NonResourceAttributes
        ] = ...,
        resource_attributes: typing.Optional[
            kubernetes.client.V1ResourceAttributes
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1SelfSubjectAccessReviewSpecDict: ...

class V1SelfSubjectAccessReviewSpecDict(typing.TypedDict, total=False):
    nonResourceAttributes: typing.Optional[
        kubernetes.client.V1NonResourceAttributesDict
    ]
    resourceAttributes: typing.Optional[kubernetes.client.V1ResourceAttributesDict]
