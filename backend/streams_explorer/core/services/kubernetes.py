from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Callable, NamedTuple, TypedDict

import kubernetes_asyncio.client
import kubernetes_asyncio.config
import kubernetes_asyncio.watch
from kubernetes_asyncio.client import (
    EventsV1Event,
    V1beta1CronJob,
    V1Deployment,
    V1StatefulSet,
)
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sObject
from streams_explorer.models.k8s import K8sDeploymentUpdateType, K8sEventType

if TYPE_CHECKING:
    from streams_explorer.streams_explorer import StreamsExplorer


class K8sResource(NamedTuple):
    resource: Callable
    return_type: type | None
    callback: Callable
    delay: int = 0


class K8sDeploymentUpdate(TypedDict):
    type: K8sDeploymentUpdateType
    object: K8sObject


class K8sEvent(TypedDict):
    type: K8sEventType
    object: EventsV1Event


class Kubernetes:
    context = settings.k8s.deployment.context
    namespaces = settings.k8s.deployment.namespaces

    def __init__(self, streams_explorer: StreamsExplorer):
        self.streams_explorer = streams_explorer

    async def setup(self):
        try:
            if settings.k8s.deployment.cluster:
                logger.info("Setup K8s environment in cluster")
                kubernetes_asyncio.config.load_incluster_config()
            else:
                logger.info("Setup K8s environment")
                await kubernetes_asyncio.config.load_kube_config(context=self.context)
        except kubernetes_asyncio.config.ConfigException as e:
            raise Exception("Could not load K8s environment configuration") from e

        conf = kubernetes_asyncio.client.Configuration.get_default_copy()
        conf.client_side_validation = False
        conf = kubernetes_asyncio.client.Configuration.set_default(conf)

        self.k8s_app_client = kubernetes_asyncio.client.AppsV1Api()
        self.k8s_batch_client = kubernetes_asyncio.client.BatchV1beta1Api()
        self.k8s_events_client = kubernetes_asyncio.client.EventsV1Api()

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

        def list_events(namespace: str, *args, **kwargs):
            return self.k8s_events_client.list_namespaced_event(
                *args, namespace=namespace, **kwargs
            )

        resources = (
            K8sResource(
                list_deployments,
                V1Deployment,
                self.streams_explorer.handle_deployment_update,
            ),
            K8sResource(
                list_stateful_sets,
                V1StatefulSet,
                self.streams_explorer.handle_deployment_update,
            ),
            K8sResource(
                list_cron_jobs,
                V1beta1CronJob,
                self.streams_explorer.handle_deployment_update,
            ),
            K8sResource(
                list_events,
                EventsV1Event,
                self.streams_explorer.handle_event,
                delay=5,
            ),
        )

        for resource, return_type, callback, delay in resources:
            await asyncio.sleep(delay)
            for namespace in self.namespaces:
                asyncio.create_task(
                    self.__watch_namespace(
                        resource,
                        namespace,
                        return_type.__name__ if return_type else None,
                        callback,
                    )
                )

    async def __watch_namespace(
        self,
        resource: Callable,
        namespace: str,
        return_type: str | None,
        callback: Callable,
    ):
        async with kubernetes_asyncio.watch.Watch(return_type) as w:
            async with w.stream(resource, namespace) as stream:
                async for event in stream:
                    await callback(event)
