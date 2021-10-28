from collections import defaultdict
from typing import Dict, List, Optional, Set

from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.models.node_information import NodeInfoListItem


class LinkingService:
    def __init__(self):
        self.sink_source_redirects: Set[str] = set()
        self._connector_info: List[NodeInfoListItem] = []
        self._streaming_app_info: List[NodeInfoListItem] = []
        self._topic_info: List[NodeInfoListItem] = []
        self._sink_source_info: Dict[str, List[NodeInfoListItem]] = defaultdict(list)

    @property
    def connector_info(self):
        return self._connector_info.copy()

    @connector_info.setter
    def connector_info(self, connector_info):
        self._connector_info = connector_info

    @property
    def streaming_app_info(self):
        return self._streaming_app_info.copy()

    @streaming_app_info.setter
    def streaming_app_info(self, streaming_app_info):
        self._streaming_app_info = streaming_app_info

    @property
    def topic_info(self):
        return self._topic_info.copy()

    @topic_info.setter
    def topic_info(self, topic_info):
        self._topic_info = topic_info

    @property
    def sink_source_info(self):
        return self._sink_source_info.copy()

    @sink_source_info.setter
    def sink_source_info(self, sink_source_info):
        self._sink_source_info = sink_source_info

    def get_redirect_connector(
        self, config: dict, link_type: Optional[str]
    ) -> Optional[str]:
        pass

    def get_redirect_topic(
        self, topic_name: str, link_type: Optional[str]
    ) -> Optional[str]:
        pass

    def get_redirect_streaming_app(
        self, k8s_app: K8sApp, link_type: Optional[str]
    ) -> Optional[str]:
        pass

    def get_sink_source_redirects(self, node_type: str, sink_source_name: str):
        pass

    def add_streaming_app_info_item(self, info_item: NodeInfoListItem):
        self._streaming_app_info.append(info_item)

    def add_connector_info_item(self, info_item: NodeInfoListItem):
        self._connector_info.append(info_item)

    def add_topic_info_item(self, info_item: NodeInfoListItem):
        self._topic_info.append(info_item)

    def add_sink_source_info_item(
        self, sink_source_type: str, info_item: NodeInfoListItem
    ):
        self._sink_source_info[sink_source_type].append(info_item)
