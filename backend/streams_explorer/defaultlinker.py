from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.models.node_information import NodeInfoListItem, NodeInfoType


class DefaultLinker(LinkingService):
    def __init__(self) -> None:
        super().__init__()
        self.sink_source_redirects = {"elasticsearch-index"}
        self.sink_source_info = {
            "elasticsearch-index": [
                NodeInfoListItem(name="Kibana", value="", type=NodeInfoType.LINK)
            ]
        }

        if settings.grafana.enable:
            self.add_topic_info_item(
                NodeInfoListItem(
                    name="Topic Monitoring", value="grafana", type=NodeInfoType.LINK
                )
            )
            grafana_consumer_link = NodeInfoListItem(
                name="Consumer Group Monitoring",
                value="grafana",
                type=NodeInfoType.LINK,
            )
            self.add_streaming_app_info_item(grafana_consumer_link)
            self.add_connector_info_item(grafana_consumer_link)

        if settings.akhq.enable:
            self.add_message_provider("akhq")
            if settings.akhq.get("connect"):
                self.add_connector_info_item(
                    NodeInfoListItem(
                        name="Connector Tasks",
                        value="akhq-connect",
                        type=NodeInfoType.LINK,
                    )
                )

        if settings.redpanda_console.enable:
            self.add_message_provider("redpanda_console")

        if settings.kibanalogs.enable:
            self.add_logging_provider("kibanalogs")

        if settings.loki.enable:
            self.add_logging_provider("loki")

    def get_redirect_connector(self, config: dict, link_type: str) -> str | None:
        if connector_name := config.get("name"):
            consumer_group = f"connect-{connector_name}"
            match link_type:
                case "grafana":
                    return f"{settings.grafana.url}/d/{settings.grafana.dashboards.consumergroups}?var-consumergroups={consumer_group}"
                case "akhq":
                    return f"{settings.akhq.url}/ui/{settings.akhq.cluster}/group/{consumer_group}"
                case "akhq-connect":
                    return f"{settings.akhq.url}/ui/{settings.akhq.cluster}/connect/{settings.akhq.get('connect')}/definition/{connector_name}/tasks"
                case "redpanda_console":
                    return f"{settings.redpanda_console.url}/groups/{consumer_group}"

    def get_redirect_topic(self, topic_name: str, link_type: str) -> str | None:
        match link_type:
            case "grafana":
                return f"{settings.grafana.url}/d/{settings.grafana.dashboards.topics}?var-topics={topic_name}"
            case "akhq":
                return (
                    f"{settings.akhq.url}/ui/{settings.akhq.cluster}/topic/{topic_name}"
                )
            case "redpanda_console":
                return f"{settings.redpanda_console.url}/topics/{topic_name}"

    def get_redirect_streaming_app(self, k8s_app: K8sApp, link_type: str) -> str | None:
        consumer_group = k8s_app.consumer_group
        match link_type:
            case "kibanalogs":
                return f"{settings.kibanalogs.url}/app/discover#/?_a=(columns:!(message),query:(language:lucene,query:'kubernetes.labels.app: \"{k8s_app.name}\"'))"
            case "loki":
                return f'{settings.loki.url}/explore?orgId=1&left=["now-1h","now","loki",{{"expr":"{{app=\\"{k8s_app.name}\\"}}"}}]'
            case "grafana" if consumer_group:
                return f"{settings.grafana.url}/d/{settings.grafana.dashboards.consumergroups}?var-consumergroups={consumer_group}"
            case "akhq" if consumer_group:
                return f"{settings.akhq.url}/ui/{settings.akhq.cluster}/group/{consumer_group}"
            case "redpanda_console" if consumer_group:
                return f"{settings.redpanda_console.url}/groups/{consumer_group}"

    def get_sink_source_redirects(
        self, node_type: str, _sink_source_name: str
    ) -> str | None:
        if node_type == "elasticsearch-index":
            return settings.esindex.url

    def add_message_provider(self, value: str) -> None:
        self.add_topic_info_item(
            NodeInfoListItem(name="Message Viewer", value=value, type=NodeInfoType.LINK)
        )
        consumer_link = NodeInfoListItem(
            name="Consumer Group Details", value=value, type=NodeInfoType.LINK
        )
        self.add_streaming_app_info_item(consumer_link)
        self.add_connector_info_item(consumer_link)

    def add_logging_provider(self, value: str) -> None:
        self.add_streaming_app_info_item(
            NodeInfoListItem(name="Logs", value=value, type=NodeInfoType.LINK),
        )
