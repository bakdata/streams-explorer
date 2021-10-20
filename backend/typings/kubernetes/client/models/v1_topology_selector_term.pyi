import datetime
import typing

import kubernetes.client

class V1TopologySelectorTerm:
    match_label_expressions: typing.Optional[
        list[kubernetes.client.V1TopologySelectorLabelRequirement]
    ]
    def __init__(
        self,
        *,
        match_label_expressions: typing.Optional[
            list[kubernetes.client.V1TopologySelectorLabelRequirement]
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1TopologySelectorTermDict: ...

class V1TopologySelectorTermDict(typing.TypedDict, total=False):
    matchLabelExpressions: typing.Optional[
        list[kubernetes.client.V1TopologySelectorLabelRequirementDict]
    ]
