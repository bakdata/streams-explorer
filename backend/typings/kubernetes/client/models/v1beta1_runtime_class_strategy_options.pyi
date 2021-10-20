import datetime
import typing

import kubernetes.client

class V1beta1RuntimeClassStrategyOptions:
    allowed_runtime_class_names: list[str]
    default_runtime_class_name: typing.Optional[str]
    def __init__(
        self,
        *,
        allowed_runtime_class_names: list[str],
        default_runtime_class_name: typing.Optional[str] = ...
    ) -> None: ...
    def to_dict(self) -> V1beta1RuntimeClassStrategyOptionsDict: ...

class V1beta1RuntimeClassStrategyOptionsDict(typing.TypedDict, total=False):
    allowedRuntimeClassNames: list[str]
    defaultRuntimeClassName: typing.Optional[str]
