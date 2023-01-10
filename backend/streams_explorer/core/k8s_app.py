from __future__ import annotations

from typing import TypeAlias

from kubernetes_asyncio.client import (
    V1beta1CronJob,
    V1Container,
    V1Deployment,
    V1Job,
    V1ObjectMeta,
    V1PodSpec,
    V1StatefulSet,
)
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_config_parser import K8sConfigParser
from streams_explorer.k8s_config_parser import load_config_parser
from streams_explorer.models.graph import AppState, ReplicaCount
from streams_explorer.models.k8s import K8sConfig, K8sReason

ATTR_PIPELINE = "pipeline"

K8sObject: TypeAlias = V1Deployment | V1StatefulSet | V1Job | V1beta1CronJob

config_parser: type[K8sConfigParser] = load_config_parser()


class K8sApp:
    def __init__(self, k8s_object: K8sObject) -> None:
        self.k8s_object = k8s_object
        self.metadata: V1ObjectMeta = k8s_object.metadata or V1ObjectMeta()
        self.attributes: dict[str, str] = {}
        self.config: K8sConfig
        self.state: K8sReason = K8sReason.UNKNOWN
        self.setup()

    @property
    def id(self) -> str:
        return self.config.id

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def input_topics(self) -> list[str]:
        return self.config.input_topics

    @property
    def output_topic(self) -> str | None:
        return self.config.output_topic

    @property
    def error_topic(self) -> str | None:
        return self.config.error_topic

    @property
    def input_pattern(self) -> str | None:
        return self.config.input_pattern

    @property
    def extra_input_topics(self) -> list[str]:
        return self.config.extra_input_topics

    @property
    def extra_output_topics(self) -> list[str]:
        return self.config.extra_output_topics

    @property
    def extra_input_patterns(self) -> list[str]:
        return self.config.extra_input_patterns

    @property
    def pipeline(self) -> str | None:
        return self.attributes.get(settings.k8s.pipeline.label)

    @property
    def consumer_group(self) -> str | None:
        return self.attributes.get(settings.k8s.consumer_group_annotation)

    @property
    def replicas_ready(self) -> int | None:
        if not self.k8s_object.status:
            return None
        return self.k8s_object.status.ready_replicas

    @property
    def replicas_total(self) -> int | None:
        if not self.k8s_object.status:
            return None
        return self.k8s_object.status.replicas

    def setup(self) -> None:
        self.spec = self._get_pod_spec()
        self._ignore_containers = self.get_ignore_containers()
        self.container = self.get_app_container(self.spec, self._ignore_containers)
        self.extract_config()
        self.__set_attributes()

    def _get_pod_spec(self) -> V1PodSpec | None:
        if self.k8s_object.spec and self.k8s_object.spec.template.spec:
            return self.k8s_object.spec.template.spec

    def extract_config(self) -> None:
        self.config = config_parser(self).parse()

    def is_streams_app(self) -> bool:
        if not self.input_topics and not self.output_topic:
            return False
        return True

    def to_dict(self) -> dict:
        return self.k8s_object.to_dict()

    def to_state_update(self) -> AppState:
        return AppState(
            id=self.id,
            replicas=ReplicaCount(self.replicas_ready, self.replicas_total),
            state=self.state,
        )

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __set_attributes(self) -> None:
        self._set_labels()
        self._set_pipeline()
        self._set_annotations()

    def _set_labels(self) -> None:
        labels = self.metadata.labels
        if not labels:
            return

        for key in self._labels_to_use():
            value = labels.get(key)
            if value is not None:
                self.attributes[key] = value
            elif self.is_streams_app():
                logger.warning(
                    f"{self.class_name} {self.name} does not have a label with the name: {key}"
                )

    def _set_pipeline(self) -> None:
        if self.pipeline:
            self.attributes[ATTR_PIPELINE] = self.pipeline

    def _set_annotations(self) -> None:
        if (
            self.k8s_object.spec
            and self.k8s_object.spec.template.metadata
            and self.k8s_object.spec.template.metadata.annotations
        ):
            annotations = self.k8s_object.spec.template.metadata.annotations
            self.attributes.update(annotations)

    @staticmethod
    def factory(k8s_object: K8sObject) -> K8sApp:
        match k8s_object:
            case V1Deployment():  # type: ignore[misc]
                return K8sAppDeployment(k8s_object)
            case V1StatefulSet():  # type: ignore[misc]
                return K8sAppStatefulSet(k8s_object)
            case V1Job():  # type: ignore[misc]
                return K8sAppJob(k8s_object)
            case V1beta1CronJob():  # type: ignore[misc]
                return K8sAppCronJob(k8s_object)
            case _:
                raise ValueError(k8s_object)

    @staticmethod
    def get_app_container(
        spec: V1PodSpec | None, ignore_containers: set[str] = set()
    ) -> V1Container | None:
        if spec and spec.containers:
            for container in spec.containers:
                if container.name not in ignore_containers:
                    return container

    @staticmethod
    def get_ignore_containers() -> set[str]:
        return {container["name"] for container in settings.k8s.containers.ignore}

    @staticmethod
    def _labels_to_use() -> set[str]:
        return set(settings.k8s.labels)


class K8sAppJob(K8sApp):
    def __init__(self, k8s_object: V1Job) -> None:
        super().__init__(k8s_object)

    def setup(self) -> None:
        self.spec = self._get_pod_spec()
        self.container = self.get_app_container(self.spec)
        self.extract_config()
        self.__set_attributes()

    @property
    def replicas_ready(self) -> None:
        return None

    @property
    def replicas_total(self) -> None:
        return None

    def _get_pod_spec(self) -> V1PodSpec | None:
        if self.k8s_object.spec and self.k8s_object.spec.template.spec:
            return self.k8s_object.spec.template.spec

    def __set_attributes(self) -> None:
        self._set_labels()
        self._set_pipeline()


class K8sAppCronJob(K8sApp):
    def __init__(self, k8s_object: V1beta1CronJob) -> None:
        super().__init__(k8s_object)

    def setup(self) -> None:
        self.spec = self._get_pod_spec()
        self.container = self.get_app_container(self.spec)
        self.extract_config()
        self.__set_attributes()

    @property
    def replicas_ready(self) -> None:
        return None

    @property
    def replicas_total(self) -> None:
        return None

    def _get_pod_spec(self) -> V1PodSpec | None:
        if (
            self.k8s_object.spec
            and self.k8s_object.spec.job_template.spec
            and self.k8s_object.spec.job_template.spec.template.spec
        ):
            return self.k8s_object.spec.job_template.spec.template.spec

    def __set_attributes(self) -> None:
        self._set_labels()
        self._set_pipeline()


class K8sAppDeployment(K8sApp):
    def __init__(self, k8s_object: V1Deployment) -> None:
        super().__init__(k8s_object)


class K8sAppStatefulSet(K8sApp):
    def __init__(self, k8s_object: V1StatefulSet) -> None:
        super().__init__(k8s_object)

    def get_service_name(self) -> str | None:
        if self.k8s_object.spec:
            return self.k8s_object.spec.service_name
