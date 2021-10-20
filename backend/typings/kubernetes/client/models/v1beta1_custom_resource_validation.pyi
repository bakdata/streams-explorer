import datetime
import typing

import kubernetes.client

class V1beta1CustomResourceValidation:
    open_apiv3_schema: typing.Optional[kubernetes.client.V1beta1JSONSchemaProps]
    def __init__(
        self,
        *,
        open_apiv3_schema: typing.Optional[
            kubernetes.client.V1beta1JSONSchemaProps
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1CustomResourceValidationDict: ...

class V1beta1CustomResourceValidationDict(typing.TypedDict, total=False):
    openAPIV3Schema: typing.Optional[kubernetes.client.V1beta1JSONSchemaPropsDict]
