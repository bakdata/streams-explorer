from typing import Dict, List, Optional

import kubernetes
from kubernetes.client import V1beta1CronJob, V1Deployment
from kubernetes.client.api_client import ApiClient
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.core.node_info_extractor import (
    get_displayed_information_connector,
    get_displayed_information_deployment,
)
from streams_explorer.core.services.dataflow_graph import DataFlowGraph, NodeTypesEnum
from streams_explorer.core.services.kafkaconnect import KafkaConnect
from streams_explorer.core.services.linking_services import LinkingService
from streams_explorer.core.services.schemaregistry import SchemaRegistry
from streams_explorer.extractors import extractor_container
from streams_explorer.models.kafka_connector import KafkaConnector
from streams_explorer.models.node_information import (
    NodeInfoListItem,
    NodeInformation,
    NodeInfoType,
)


class StreamsExplorer:
    k8s_app_client: Optional[ApiClient] = None
    k8s_batch_client: Optional[ApiClient] = None
    v1_client: Optional[ApiClient] = None
    context = settings.k8s.deployment.context
    namespaces = settings.k8s.deployment.namespaces

    def __init__(self, linking_service: LinkingService):
        self.applications: Dict[str, K8sApp] = {}
        self.kafka_connectors: List[KafkaConnector] = []
        self.data_flow = DataFlowGraph()
        self.linking_service = linking_service

    def setup(self):
        self.__setup_k8s_environment()

    def update(self):
        self.applications = {}
        self.kafka_connectors = []
        self.data_flow.reset()
        self.__retrieve_deployments()
        self.__retrieve_cron_jobs()
        self.__get_connectors()
        self.__create_graph()

    def get_positioned_json_graph(self) -> dict:
        return self.data_flow.get_positioned_graph()

    def get_positioned_pipeline_json_graph(self, pipeline_name) -> dict:
        return self.data_flow.get_positioned_pipeline_graph(pipeline_name)

    def get_pipeline_names(self) -> List[str]:
        return list(self.data_flow.independent_graphs.keys())

    def get_metrics(self) -> List:
        return self.data_flow.get_metrics()

    def get_node_information(self, node_id: str):
        node_type = self.data_flow.get_node_type(node_id)
        if node_type == NodeTypesEnum.CONNECTOR:
            _, config = KafkaConnect.get_connector_info(node_id)
            return NodeInformation(
                node_id=node_id,
                node_type=node_type,
                info=self.linking_service.connector_info
                + get_displayed_information_connector(config),
            )
        if node_type == NodeTypesEnum.TOPIC or node_type == NodeTypesEnum.ERROR_TOPIC:
            return NodeInformation(
                node_id=node_id,
                node_type=node_type,
                info=self.linking_service.topic_info
                + [
                    NodeInfoListItem(
                        name="Schema",
                        value=SchemaRegistry.get_newest_topic_value_schema(node_id),
                        type=NodeInfoType.JSON,
                    )
                ],
            )
        if node_type == NodeTypesEnum.STREAMING_APP:
            info = get_displayed_information_deployment(self.applications[node_id])
            return NodeInformation(
                node_id=node_id,
                node_type=node_type,
                info=self.linking_service.streaming_app_info + info,
            )

        if node_type in self.linking_service.sink_source_info:
            return NodeInformation(
                node_id=node_id,
                node_type=NodeTypesEnum.SINK_SOURCE,
                info=self.linking_service.sink_source_info[node_type],
            )

    def get_link(self, node_id: str, link_type: Optional[str]):
        node_type = self.data_flow.get_node_type(node_id)
        if node_type == NodeTypesEnum.CONNECTOR:
            _, config = KafkaConnect.get_connector_info(node_id)
            return self.linking_service.get_redirect_connector(config, link_type)
        if node_type == NodeTypesEnum.TOPIC or node_type == NodeTypesEnum.ERROR_TOPIC:
            return self.linking_service.get_redirect_topic(node_id, link_type)
        if node_type == NodeTypesEnum.STREAMING_APP:
            return self.linking_service.get_redirect_streaming_app(
                self.applications[node_id], link_type
            )

        if node_type in self.linking_service.sink_source_redirects:
            return self.linking_service.get_sink_source_redirects(node_type, node_id)

    def __setup_k8s_environment(self):
        try:
            if settings.k8s.deployment.cluster:
                logger.info("Setup K8s environment in cluster")
                kubernetes.config.load_incluster_config()
            else:
                logger.info("Setup K8s environment")
                kubernetes.config.load_kube_config(context=self.context)
        except kubernetes.config.ConfigException:
            raise Exception("Could not load K8s environment configuration")

        self.k8s_app_client = kubernetes.client.AppsV1Api()
        self.k8s_batch_client = kubernetes.client.BatchV1beta1Api()

    def __retrieve_deployments(self):
        logger.info("Retrieve deployment descriptions")
        deployments = self.get_deployments()
        for item in deployments:
            try:
                app = K8sApp(item)
                if app.is_common_streams_app():
                    self.applications[app.name] = app
            except Exception as e:
                logger.debug(e)

    def get_deployments(self) -> List[V1Deployment]:
        deployments: List[V1Deployment] = []
        for namespace in self.namespaces:
            logger.info(f"List deployments in namespace {namespace}")
            deployments += self.k8s_app_client.list_namespaced_deployment(
                namespace=namespace, watch=False
            ).items
        return deployments

    def __retrieve_cron_jobs(self):
        logger.info("Retrieve cronjob descriptions")
        cron_jobs = self.get_cron_jobs()
        for cron_job in cron_jobs:
            extractor_container.on_cron_job(cron_job)

    def get_cron_jobs(self) -> List[V1beta1CronJob]:
        cron_jobs: List[V1beta1CronJob] = []
        for namespace in self.namespaces:
            logger.info(f"List cronjobs in namespace {namespace}")
            cron_jobs += self.k8s_batch_client.list_namespaced_cron_job(
                namespace=namespace, watch=False
            ).items
        return cron_jobs

    def __get_connectors(self):
        logger.info("Retrieve Kafka connectors")
        self.kafka_connectors = KafkaConnect.connectors()

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

        # extract subgraphs
        logger.info("Extract independent pipelines")
        self.data_flow.extract_independent_pipelines()
