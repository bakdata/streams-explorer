from typing import Optional

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.models.node_information import NodeInfoListItem, NodeInfoType


class DefaultLinker(LinkingService):
    sink_source_redirects = {"elasticsearch-index"}

    def __init__(self):
        grafana_consumer_link = NodeInfoListItem(
            name="Consumer Group Monitoring", value="grafana", type=NodeInfoType.LINK
        )
        self.topic_info = [
            NodeInfoListItem(
                name="Topic Monitoring", value="grafana", type=NodeInfoType.LINK
            ),
            NodeInfoListItem(
                name="Message Viewer", value="akhq", type=NodeInfoType.LINK
            ),
        ]
        self.streaming_app_info = [
            grafana_consumer_link,
            NodeInfoListItem(
                name="Kibana Logs", value="kibanalogs", type=NodeInfoType.LINK
            ),
        ]
        self.connector_info = [grafana_consumer_link]
        self.sink_source_info = {
            "elasticsearch-index": [
                NodeInfoListItem(name="Kibana", value="", type=NodeInfoType.LINK)
            ]
        }

    def get_redirect_connector(
        self, config: dict, link_type: Optional[str]
    ) -> Optional[str]:
        if link_type == "grafana":
            connector_name = config.get("name")
            if connector_name is not None:
                return f"{settings.grafana.url}/d/{settings.grafana.dashboards.consumergroups}?var-consumergroups=connect-{connector_name}"
        return None

    def get_redirect_topic(
        self, topic_name: str, link_type: Optional[str]
    ) -> Optional[str]:
        if link_type == "akhq":
            return f"{settings.akhq.url}/ui/{settings.akhq.cluster}/topic/{topic_name}"
        if link_type == "grafana":
            return f"{settings.grafana.url}/d/{settings.grafana.dashboards.topics}?var-topics={topic_name}"
        return None

    def get_redirect_streaming_app(
        self, k8s_application: K8sApp, link_type: Optional[str]
    ) -> Optional[str]:
        if link_type == "kibanalogs":
            return f"{settings.kibanalogs.url}/app/kibana#/discover?_a=(columns:!(_source),query:(language:lucene,query:'kubernetes.labels.app:%20%22{k8s_application.metadata.labels.get('app')}%22'))"
        if link_type == "grafana":
            consumer_group = k8s_application.attributes.get(
                settings.k8s.consumer_group_annotation
            )
            if consumer_group is not None:
                return f"{settings.grafana.url}/d/{settings.grafana.dashboards.consumergroups}?var-consumergroups={consumer_group}"
        return None

    def get_sink_source_redirects(self, node_type: str, sink_source_name: str):
        if node_type == "elasticsearch-index":
            return settings.esindex.url
