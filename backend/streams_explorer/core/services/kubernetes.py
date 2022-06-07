import asyncio
from typing import TYPE_CHECKING, Callable, TypedDict

import kubernetes_asyncio.client
import kubernetes_asyncio.config
import kubernetes_asyncio.watch
from kubernetes_asyncio.client import V1beta1CronJob, V1Deployment, V1StatefulSet
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sObject
from streams_explorer.models.k8s import K8sEventType

if TYPE_CHECKING:
    from streams_explorer.streams_explorer import StreamsExplorer


class K8sEvent(TypedDict):
    type: K8sEventType
    object: K8sObject


class Kubernetes:
    context = settings.k8s.deployment.context
    namespaces = settings.k8s.deployment.namespaces

    def __init__(self, streams_explorer):
        self.streams_explorer: StreamsExplorer = streams_explorer

    async def setup(self):
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
                    self.__watch_namespace(resource, namespace, return_type.__name__)
                )

    async def __watch_namespace(
        self, resource: Callable, namespace: str, return_type: str
    ):
        async with kubernetes_asyncio.watch.Watch(return_type=return_type) as w:
            async with w.stream(resource, namespace) as stream:
                async for event in stream:
                    self.streams_explorer.handle_event(
                        event  # pyright: ignore[reportGeneralTypeIssues]
                    )
