import asyncio
from typing import Dict, List, Optional, Type

import kubernetes_asyncio.client
import kubernetes_asyncio.config
import kubernetes_asyncio.watch
from cachetools.func import ttl_cache
from kubernetes_asyncio.client import V1beta1CronJob, V1Deployment, V1StatefulSet
from loguru import logger

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
from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.core.services.metric_providers import MetricProvider
from streams_explorer.extractors import extractor_container
from streams_explorer.models.graph import Metric
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.node_information import (
    NodeInfoListItem,
    NodeInformation,
    NodeInfoType,
)


class StreamsExplorer:
    context = settings.k8s.deployment.context
    namespaces = settings.k8s.deployment.namespaces

    def __init__(
        self, linking_service: LinkingService, metric_provider: Type[MetricProvider]
    ):
        self.applications: Dict[str, K8sApp] = {}
        self.kafka_connectors: List[KafkaConnector] = []
        self.kafka = KafkaAdminClient()
        self.data_flow = DataFlowGraph(
            metric_provider=metric_provider, kafka=self.kafka
        )
        self.linking_service = linking_service

    async def setup(self):
        await self.__setup_k8s_environment()

    async def watch(self):
        def list_deployments(namespace: str, *args, **kwargs):
            return self.k8s_app_client.list_namespaced_deployment(
                *args, namespace=namespace, **kwargs
            )

        def list_stateful_sets(namespace: str, *args, **kwargs):
            return self.k8s_app_client.list_namespaced_stateful_set(
                *args, namespace=namespace, **kwargs
            )

        def list_cron_jobs(namespace: str, *args, **kwargs):
            return self.k8s_batch_client.list_namespaced_cron_job(
                *args, namespace=namespace, **kwargs
            )

        resources = (
            (list_deployments, V1Deployment),
            (list_stateful_sets, V1StatefulSet),
            (list_cron_jobs, V1beta1CronJob),
        )

        for resource, return_type in resources:
            for namespace in self.namespaces:
                asyncio.create_task(
                    self.__watch_k8s(resource, namespace, return_type.__name__)
                )

    async def update(self):
        # extractor_container.reset()
        self.data_flow.reset()
        self.__create_graph()
        self.data_flow.setup_metric_provider()
        await self.data_flow.store_json_graph()

    def get_positioned_json_graph(self) -> dict:
        return self.data_flow.json_graph

    async def get_positioned_pipeline_json_graph(
        self, pipeline_name: str
    ) -> Optional[dict]:
        return await self.data_flow.get_positioned_pipeline_graph(pipeline_name)

    def get_pipeline_names(self) -> List[str]:
        return list(self.data_flow.pipelines.keys())

    async def get_metrics(self) -> List[Metric]:
        return await self.data_flow.get_metrics()

    @ttl_cache(ttl=settings.node_info.cache_ttl)
    def get_node_information(self, node_id: str):
        node_type = self.data_flow.get_node_type(node_id)

        if node_type == NodeTypesEnum.CONNECTOR:
            config = KafkaConnect.get_connector_config(node_id)
            return NodeInformation(
                node_id=node_id,
                node_type=node_type,
                info=self.linking_service.connector_info
                + get_displayed_information_connector(config),
            )

        elif node_type == NodeTypesEnum.TOPIC or node_type == NodeTypesEnum.ERROR_TOPIC:
            info = self.linking_service.topic_info
            if self.kafka.enabled:
                partitions = self.kafka.get_topic_partitions(node_id)
                if partitions is not None:
                    info.append(
                        NodeInfoListItem(
                            name="Partitions",
                            value=len(partitions),
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

        elif node_type == NodeTypesEnum.STREAMING_APP:
            info = get_displayed_information_deployment(self.applications[node_id])
            return NodeInformation(
                node_id=node_id,
                node_type=node_type,
                info=self.linking_service.streaming_app_info + info,
            )

        elif node_type in self.linking_service.sink_source_info:
            return NodeInformation(
                node_id=node_id,
                node_type=NodeTypesEnum.SINK_SOURCE,
                info=self.linking_service.sink_source_info[node_type],
            )

    def get_link(self, node_id: str, link_type: Optional[str]):
        node_type = self.data_flow.get_node_type(node_id)
        if node_type == NodeTypesEnum.CONNECTOR:
            config = KafkaConnect.get_connector_config(node_id)
            return self.linking_service.get_redirect_connector(config, link_type)
        if node_type == NodeTypesEnum.TOPIC or node_type == NodeTypesEnum.ERROR_TOPIC:
            return self.linking_service.get_redirect_topic(node_id, link_type)
        if node_type == NodeTypesEnum.STREAMING_APP:
            return self.linking_service.get_redirect_streaming_app(
                self.applications[node_id], link_type
            )

        if node_type in self.linking_service.sink_source_redirects:
            return self.linking_service.get_sink_source_redirects(node_type, node_id)

    async def __setup_k8s_environment(self):
        try:
            if settings.k8s.deployment.cluster:
                logger.info("Setup K8s environment in cluster")
                kubernetes_asyncio.config.load_incluster_config()
            else:
                logger.info("Setup K8s environment")
                await kubernetes_asyncio.config.load_kube_config(context=self.context)
        except kubernetes_asyncio.config.ConfigException:
            raise Exception("Could not load K8s environment configuration")

        self.k8s_app_client = kubernetes_asyncio.client.AppsV1Api()
        self.k8s_batch_client = kubernetes_asyncio.client.BatchV1beta1Api()

    async def __watch_k8s(self, resource, namespace: str, return_type: str):
        async with kubernetes_asyncio.watch.Watch(return_type=return_type) as w:
            async with w.stream(resource, namespace) as stream:
                async for event in stream:
                    self.handle_event(event)

    def handle_event(self, event: dict) -> None:
        item = event["object"]
        logger.info(
            f"{item.metadata.namespace} {item.__class__.__name__} {event['type']}: {item.metadata.name}"
        )

        # cronjobs need special treatment
        if isinstance(item, V1beta1CronJob):
            if app := extractor_container.on_cron_job(item):
                if event["type"] in ("ADDED", "MODIFIED"):
                    self.__add_app(app)
                elif event["type"] == "DELETED":
                    self.__remove_app(app)
                return

        app = K8sApp.factory(item)
        if event["type"] in ("ADDED", "MODIFIED"):
            self.__add_app(app)
        elif event["type"] == "DELETED":
            self.__remove_app(app)

    def get_deployments(self) -> List[V1Deployment]:
        deployments: List[V1Deployment] = []
        for namespace in self.namespaces:
            logger.info(f"List deployments in namespace {namespace}")
            deployments += self.k8s_app_client.list_namespaced_deployment(
                namespace=namespace, watch=False
            ).items
        return deployments

    def get_stateful_sets(self) -> List[V1StatefulSet]:
        stateful_sets: List[V1StatefulSet] = []
        for namespace in self.namespaces:
            logger.info(f"List statefulsets in namespace {namespace}")
            stateful_sets += self.k8s_app_client.list_namespaced_stateful_set(
                namespace=namespace, watch=False
            ).items
        return stateful_sets

    def __retrieve_cron_jobs(self):
        logger.info("Retrieve cronjob descriptions")
        cron_jobs = self.get_cron_jobs()
        for cron_job in cron_jobs:
            if app := extractor_container.on_cron_job(cron_job):
                self.__add_app(app)

    def get_cron_jobs(self) -> List[V1beta1CronJob]:
        cron_jobs: List[V1beta1CronJob] = []
        for namespace in self.namespaces:
            logger.info(f"List cronjobs in namespace {namespace}")
            cron_jobs += self.k8s_batch_client.list_namespaced_cron_job(
                namespace=namespace, watch=False
            ).items
        return cron_jobs

    def update_connectors(self):
        self.kafka_connectors.clear()
        logger.info("Retrieve Kafka connectors")
        self.kafka_connectors = KafkaConnect.connectors()

    def __add_app(self, app: K8sApp):
        if app.is_streams_bootstrap_app():
            self.applications[app.id] = app

    def __remove_app(self, app: K8sApp):
        self.applications.pop(app.id)

    def __create_graph(self):
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
