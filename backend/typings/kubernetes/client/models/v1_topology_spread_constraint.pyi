import datetime
import typing

import kubernetes.client

class V1TopologySpreadConstraint:
    label_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    max_skew: int
    topology_key: str
    when_unsatisfiable: str
    def __init__(
        self,
        *,
        label_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...,
        max_skew: int,
        topology_key: str,
        when_unsatisfiable: str
    ) -> None: ...
    def to_dict(self) -> V1TopologySpreadConstraintDict: ...

class V1TopologySpreadConstraintDict(typing.TypedDict, total=False):
    labelSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    maxSkew: int
    topologyKey: str
    whenUnsatisfiable: str
