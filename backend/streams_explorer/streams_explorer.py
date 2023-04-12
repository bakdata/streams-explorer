import re

from cachetools.func import ttl_cache
from fastapi import WebSocket
from kubernetes_asyncio.client import V1beta1CronJob, V1Job
from loguru import logger

from streams_explorer.core.client_manager import ClientManager
from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.node_info_extractor import (
    get_displayed_information_connector,
    get_displayed_information_deployment,
    get_displayed_information_topic,
)
from streams_explorer.core.services.dataflow_graph import DataFlowGraph, NodeTypesEnum
from streams_explorer.core.services.kafka_admin_client import KafkaAdminClient
from streams_explorer.core.services.kafkaconnect import KafkaConnect
from streams_explorer.core.services.kubernetes import (
    K8sDeploymentUpdate,
    K8sEvent,
    Kubernetes,
)
from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.core.services.metric_providers import MetricProvider
from streams_explorer.extractors import extractor_container
from streams_explorer.models.graph import Metric
from streams_explorer.models.k8s import K8sDeploymentUpdateType, K8sReason
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.node_information import (
    NodeInfoListItem,
    NodeInformation,
    NodeInfoType,
)


class StreamsExplorer:
    def __init__(
        self, linking_service: LinkingService, metric_provider: type[MetricProvider]
    ) -> None:
        self.applications: dict[str, K8sApp] = {}
        self.kafka_connectors: list[KafkaConnector] = []
        self.kubernetes = Kubernetes(self)
        self.kafka = KafkaAdminClient()
        self.data_flow = DataFlowGraph(
            metric_provider=metric_provider, kafka=self.kafka
        )
        self.linking_service = linking_service
        self.client_manager = ClientManager()
        self.modified: bool = True

    async def setup(self) -> None:
        await self.kubernetes.setup()

    async def watch(self) -> None:
        await self.kubernetes.watch()

    async def update_graph(self) -> None:
        if not self.modified:
            return  # skip unnecessary re-render
        logger.info("Update graph")
        self.data_flow.reset()
        self.__create_graph()
        self.modified = False
        self.data_flow.setup_metric_provider()
        await self.data_flow.store_json_graph()
        logger.info("Update graph completed")

    def get_positioned_json_graph(self) -> dict:
        return self.data_flow.json_graph

    async def get_positioned_pipeline_json_graph(self, pipeline_name: str) -> dict:
        return await self.data_flow.get_positioned_pipeline_graph(pipeline_name)

    def get_pipeline_names(self) -> list[str]:
        return list(sorted(self.data_flow.pipelines.keys()))

    async def get_metrics(self) -> list[Metric]:
        return await self.data_flow.get_metrics()

    @ttl_cache(ttl=settings.node_info.cache_ttl)
    def get_node_information(self, node_id: str) -> NodeInformation | None:
        node_type = self.data_flow.get_node_type(node_id)

        match node_type:
            case NodeTypesEnum.CONNECTOR:
                config = KafkaConnect.get_connector_config(node_id)
                return NodeInformation(
                    node_id=node_id,
                    node_type=node_type,
                    info=self.linking_service.connector_info
                    + get_displayed_information_connector(config),
                )

            case NodeTypesEnum.TOPIC | NodeTypesEnum.ERROR_TOPIC:
                info = self.linking_service.topic_info
                if self.kafka.enabled:
                    partitions = self.kafka.get_topic_partitions(node_id)
                    if partitions is not None:
                        info.append(
                            NodeInfoListItem(
                                name="Partitions",
                                value=str(len(partitions)),
                                type=NodeInfoType.BASIC,
                            )
                        )
                    config = self.kafka.get_topic_config(node_id)
                    info += get_displayed_information_topic(config)
                info.append(
                    NodeInfoListItem(
                        name="Schema",
                        value={},
                        type=NodeInfoType.JSON,
                    )
                )
                return NodeInformation(
                    node_id=node_id,
                    node_type=node_type,
                    info=info,
                )

            case NodeTypesEnum.STREAMING_APP:
                info = get_displayed_information_deployment(self.applications[node_id])
                return NodeInformation(
                    node_id=node_id,
                    node_type=node_type,
                    info=self.linking_service.streaming_app_info + info,
                )

            case sink_source if sink_source in self.linking_service.sink_source_info:
                return NodeInformation(
                    node_id=node_id,
                    node_type=NodeTypesEnum.SINK_SOURCE,
                    info=self.linking_service.sink_source_info[node_type],
                )

    def get_link(self, node_id: str, link_type: str) -> str | None:
        node_type = self.data_flow.get_node_type(node_id)
        match node_type:
            case NodeTypesEnum.CONNECTOR:
                config = KafkaConnect.get_connector_config(node_id)
                return self.linking_service.get_redirect_connector(config, link_type)
            case NodeTypesEnum.TOPIC | NodeTypesEnum.ERROR_TOPIC:
                return self.linking_service.get_redirect_topic(node_id, link_type)
            case NodeTypesEnum.STREAMING_APP:
                return self.linking_service.get_redirect_streaming_app(
                    self.applications[node_id], link_type
                )
        if node_type in self.linking_service.sink_source_redirects:
            return self.linking_service.get_sink_source_redirects(node_type, node_id)

    async def handle_deployment_update(self, update: K8sDeploymentUpdate) -> None:
        item = update["object"]
        logger.info(
            f"{item.metadata.namespace} {item.__class__.__name__} {update['type']}: {item.metadata.name}"  # pyright: ignore[reportOptionalMemberAccess]
        )

        app: K8sApp | None = None
        match item:
            case V1Job():  # type: ignore[misc]
                app = extractor_container.on_job(item)
            case V1beta1CronJob():  # type: ignore[misc]
                app = extractor_container.on_cron_job(item)
            case _:
                app = K8sApp.factory(item)
        if app:
            await self._handle_app_update(update["type"], app)

    async def _handle_app_update(
        self, type: K8sDeploymentUpdateType, app: K8sApp
    ) -> None:
        match type:
            case K8sDeploymentUpdateType.ADDED | K8sDeploymentUpdateType.MODIFIED:
                await self.__add_app(app)
            case K8sDeploymentUpdateType.DELETED:
                self.__remove_app(app)

    async def handle_event(self, raw_event: K8sEvent) -> None:
        event = raw_event["object"]

        # extract deployment name from pod
        if not event.reason or not event.regarding or not event.regarding.field_path:
            return
        name = re.findall(r"{(.+?)}", event.regarding.field_path)[0]

        logger.info(
            "{} {} {} ({})",
            event.regarding.namespace,
            name,
            event.reason,
            event.type,
        )
        logger.debug(event)

        # map event to application
        if app := self.applications.get(name):
            app.state = K8sReason.from_str(event.reason)
            # app.note = event["note"] # TODO
            await self._update_clients_delta(app)

    def update_connectors(self) -> None:
        extractor_container.reset_connectors()
        logger.info("Retrieve Kafka connectors")
        self.kafka_connectors = KafkaConnect.connectors()
        self.modified = True

    async def update_client_full(self, client: WebSocket) -> None:
        """Send all current application states to client."""
        for app in self.applications.values():
            await self.client_manager.send(client, app.to_state_update())

    async def _update_clients_delta(self, app: K8sApp) -> None:
        """Broadcast a new application state to clients."""
        await self.client_manager.broadcast(app.to_state_update())

    async def __add_app(self, app: K8sApp) -> None:
        if app.is_streams_app():
            self.applications[app.id] = app
            self.modified = True
            extractor_container.on_streaming_app_add(app.config)
            await self._update_clients_delta(app)

    def __remove_app(self, app: K8sApp) -> None:
        if app.is_streams_app():
            self.applications.pop(app.id)
            self.modified = True
            extractor_container.on_streaming_app_delete(app.config)

    def __create_graph(self) -> None:
        logger.info("Setup pipeline graph")
        for _, app in self.applications.items():
            self.data_flow.add_streaming_app(app)

        for connector in self.kafka_connectors:
            self.data_flow.add_connector(connector)

        sources, sinks = extractor_container.get_sources_sinks()
        for source in sources:
            self.data_flow.add_source(source)

        for sink in sinks:
            self.data_flow.add_sink(sink)

        self.data_flow.apply_input_pattern_edges()
