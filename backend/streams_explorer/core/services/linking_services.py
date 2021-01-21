from abc import abstractmethod
from typing import Dict, List, Optional

from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.models.node_information import NodeInfoListItem


class LinkingService:
    sink_source_redirects: set = set()
    connector_info: List[NodeInfoListItem] = []
    streaming_app_info: List[NodeInfoListItem] = []
    topic_info: List[NodeInfoListItem] = []
    sink_source_info: Dict[str, List[NodeInfoListItem]] = {}

    @abstractmethod
    def get_redirect_connector(
        self, config: dict, link_type: Optional[str]
    ) -> Optional[str]:
        pass

    @abstractmethod
    def get_redirect_topic(
        self, topic_name: str, link_type: Optional[str]
    ) -> Optional[str]:
        pass

    @abstractmethod
    def get_redirect_streaming_app(
        self, k8s_application: K8sApp, link_type: Optional[str]
    ) -> Optional[str]:
        pass

    @abstractmethod
    def get_sink_source_redirects(self, node_type: str, sink_source_name: str):
        pass

    @staticmethod
    def add_streaming_app_info_item(info_item: NodeInfoListItem):
        LinkingService.streaming_app_info.append(info_item)

    @staticmethod
    def add_connector_info_item(info_item: NodeInfoListItem):
        LinkingService.connector_info.append(info_item)

    @staticmethod
    def add_topic_info_item(info_item: NodeInfoListItem):
        LinkingService.topic_info.append(info_item)

    @staticmethod
    def add_sink_source_info_item(sink_source_type: str, info_item: NodeInfoListItem):
        if sink_source_type not in LinkingService.sink_source_info:
            LinkingService.sink_source_info[sink_source_type] = [info_item]
        else:
            LinkingService.sink_source_info[sink_source_type].append(info_item)
