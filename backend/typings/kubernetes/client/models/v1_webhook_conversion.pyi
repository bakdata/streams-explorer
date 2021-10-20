import datetime
import typing

import kubernetes.client

class V1WebhookConversion:
    client_config: typing.Optional[kubernetes.client.ApiextensionsV1WebhookClientConfig]
    conversion_review_versions: list[str]
    def __init__(
        self,
        *,
        client_config: typing.Optional[
            kubernetes.client.ApiextensionsV1WebhookClientConfig
        ] = ...,
        conversion_review_versions: list[str]
    ) -> None: ...
    def to_dict(self) -> V1WebhookConversionDict: ...

class V1WebhookConversionDict(typing.TypedDict, total=False):
    clientConfig: typing.Optional[
        kubernetes.client.ApiextensionsV1WebhookClientConfigDict
    ]
    conversionReviewVersions: list[str]
