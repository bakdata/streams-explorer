from abc import abstractmethod
from collections import defaultdict

from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.models.node_information import NodeInfoListItem
from streams_explorer.plugins import Plugin


class LinkingService(Plugin):
    def __init__(self) -> None:
        self.sink_source_redirects: set[str] = set()
        self._connector_info: list[NodeInfoListItem] = []
        self._streaming_app_info: list[NodeInfoListItem] = []
        self._topic_info: list[NodeInfoListItem] = []
        self._sink_source_info: defaultdict[str, list[NodeInfoListItem]] = defaultdict(
            list
        )

    @property
    def connector_info(self) -> list[NodeInfoListItem]:
        return self._connector_info.copy()

    @connector_info.setter
    def connector_info(self, connector_info: list[NodeInfoListItem]) -> None:
        self._connector_info = connector_info

    @property
    def streaming_app_info(self) -> list[NodeInfoListItem]:
        return self._streaming_app_info.copy()

    @streaming_app_info.setter
    def streaming_app_info(self, streaming_app_info: list[NodeInfoListItem]) -> None:
        self._streaming_app_info = streaming_app_info

    @property
    def topic_info(self) -> list[NodeInfoListItem]:
        return self._topic_info.copy()

    @topic_info.setter
    def topic_info(self, topic_info: list[NodeInfoListItem]) -> None:
        self._topic_info = topic_info

    @property
    def sink_source_info(self) -> dict[str, list[NodeInfoListItem]]:
        return self._sink_source_info.copy()

    @sink_source_info.setter
    def sink_source_info(
        self, sink_source_info: dict[str, list[NodeInfoListItem]]
    ) -> None:
        self._sink_source_info = defaultdict(list, sink_source_info)

    @abstractmethod
    def get_redirect_connector(self, config: dict, link_type: str) -> str | None:
        ...

    @abstractmethod
    def get_redirect_topic(self, topic_name: str, link_type: str) -> str | None:
        ...

    @abstractmethod
    def get_redirect_streaming_app(self, k8s_app: K8sApp, link_type: str) -> str | None:
        ...

    @abstractmethod
    def get_sink_source_redirects(
        self, node_type: str, sink_source_name: str
    ) -> str | None:
        ...

    def add_streaming_app_info_item(self, info_item: NodeInfoListItem) -> None:
        self._streaming_app_info.append(info_item)

    def add_connector_info_item(self, info_item: NodeInfoListItem) -> None:
        self._connector_info.append(info_item)

    def add_topic_info_item(self, info_item: NodeInfoListItem) -> None:
        self._topic_info.append(info_item)

    def add_sink_source_info_item(
        self, sink_source_type: str, info_item: NodeInfoListItem
    ) -> None:
        self._sink_source_info[sink_source_type].append(info_item)
