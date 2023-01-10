from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Awaitable, Callable, NamedTuple, TypedDict

import kubernetes_asyncio.client
import kubernetes_asyncio.config
import kubernetes_asyncio.watch
from kubernetes_asyncio.client import (
    ApiException,
    EventsV1Event,
    EventsV1EventList,
    V1beta1CronJob,
    V1beta1CronJobList,
    V1Deployment,
    V1DeploymentList,
    V1Job,
    V1JobList,
    V1StatefulSet,
    V1StatefulSetList,
)
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sObject
from streams_explorer.models.k8s import K8sDeploymentUpdateType, K8sEventType

if TYPE_CHECKING:
    from streams_explorer.streams_explorer import StreamsExplorer


class K8sResource(NamedTuple):
    func: Callable[
        ...,
        V1DeploymentList
        | V1StatefulSetList
        | V1JobList
        | V1beta1CronJobList
        | EventsV1EventList,
    ]
    return_type: type | None
    callback: Callable[..., Awaitable[None]]
    delay: int = 0


class K8sDeploymentUpdate(TypedDict):
    type: K8sDeploymentUpdateType
    object: K8sObject


class K8sEvent(TypedDict):
    type: K8sEventType
    object: EventsV1Event


class Kubernetes:
    context: str = settings.k8s.deployment.context
    namespaces: list[str] = settings.k8s.deployment.namespaces

    def __init__(self, streams_explorer: StreamsExplorer) -> None:
        self.streams_explorer = streams_explorer

    async def setup(self) -> None:
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
        kubernetes_asyncio.client.Configuration.set_default(conf)

        self.k8s_app_client = kubernetes_asyncio.client.AppsV1Api()
        self.k8s_batch_client = kubernetes_asyncio.client.BatchV1Api()
        self.k8s_beta_batch_client = kubernetes_asyncio.client.BatchV1beta1Api()
        self.k8s_events_client = kubernetes_asyncio.client.EventsV1Api()

    async def watch(self) -> None:
        def list_deployments(namespace: str, *args, **kwargs) -> V1DeploymentList:
            return self.k8s_app_client.list_namespaced_deployment(
                *args, namespace=namespace, **kwargs
            )

        def list_stateful_sets(namespace: str, *args, **kwargs) -> V1StatefulSetList:
            return self.k8s_app_client.list_namespaced_stateful_set(
                *args, namespace=namespace, **kwargs
            )

        def list_jobs(namespace: str, *args, **kwargs) -> V1JobList:
            return self.k8s_batch_client.list_namespaced_job(
                *args, namespace=namespace, **kwargs
            )

        def list_cron_jobs(namespace: str, *args, **kwargs) -> V1beta1CronJobList:
            return self.k8s_beta_batch_client.list_namespaced_cron_job(
                *args, namespace=namespace, **kwargs
            )

        def list_events(namespace: str, *args, **kwargs) -> EventsV1EventList:
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
                list_jobs,
                V1Job,
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

        for resource in resources:
            await asyncio.sleep(resource.delay)
            for namespace in self.namespaces:
                asyncio.create_task(
                    self.__watch_namespace(
                        namespace,
                        resource,
                    )
                )

    async def __watch_namespace(
        self,
        namespace: str,
        resource: K8sResource,
    ) -> None:
        return_type = resource.return_type.__name__ if resource.return_type else None
        try:
            async with kubernetes_asyncio.watch.Watch(return_type) as w:
                async with w.stream(resource.func, namespace) as stream:
                    async for event in stream:
                        await resource.callback(event)
        except ApiException as e:
            if e.status == 410:
                # restart watch to get fresh resource version
                return await self.__watch_namespace(namespace, resource)
            else:
                raise
