from __future__ import annotations

from typing import Dict, Optional, Set, Type, Union

from kubernetes_asyncio.client import (
    V1beta1CronJob,
    V1Container,
    V1Deployment,
    V1ObjectMeta,
    V1PodSpec,
    V1StatefulSet,
)
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_config_parser import K8sConfigParser
from streams_explorer.k8s_config_parser import load_config_parser
from streams_explorer.models.k8s import K8sConfig

ATTR_PIPELINE = "pipeline"

K8sObject = Union[V1Deployment, V1StatefulSet, V1beta1CronJob]

config_parser: Type[K8sConfigParser] = load_config_parser()


class K8sApp:
    def __init__(self, k8s_object: K8sObject):
        self.k8s_object = k8s_object
        self.metadata: V1ObjectMeta = k8s_object.metadata or V1ObjectMeta()
        self.attributes: Dict[str, str] = {}
        self.config: K8sConfig
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

    def setup(self):
        self.spec = self._get_pod_spec()
        self._ignore_containers = self.get_ignore_containers()
        self.container = self.get_app_container(self.spec, self._ignore_containers)
        self.extract_config()
        self.__get_attributes()

    def _get_pod_spec(self) -> V1PodSpec | None:
        if self.k8s_object.spec and self.k8s_object.spec.template.spec:
            return self.k8s_object.spec.template.spec

    def extract_config(self) -> None:
        self.config = config_parser(self).parse()

    def to_dict(self) -> dict:
        return self.k8s_object.to_dict()

    def get_pipeline(self) -> Optional[str]:
        return self.attributes.get(settings.k8s.pipeline.label)

    def get_consumer_group(self) -> Optional[str]:
        return self.attributes.get(settings.k8s.consumer_group_annotation)

    def is_streams_bootstrap_app(self) -> bool:
        if not self.input_topics and not self.output_topic:
            return False
        return True

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __get_attributes(self):
        labels = self.metadata.labels or {}
        labels_to_use = self.get_labels()

        for key in labels_to_use:
            value = labels.get(key)
            if value is not None:
                self.attributes[key] = value
            elif self.is_streams_bootstrap_app():
                logger.warning(
                    f"{self.class_name} {self.name} does not have a label with the name: {key}"
                )

        pipeline = self.get_pipeline()
        if pipeline is not None:
            self.attributes[ATTR_PIPELINE] = pipeline

        if (
            self.k8s_object.spec
            and self.k8s_object.spec.template.metadata
            and self.k8s_object.spec.template.metadata.annotations
        ):
            annotations = self.k8s_object.spec.template.metadata.annotations
            self.attributes.update(annotations)

    @staticmethod
    def factory(k8s_object: K8sObject) -> K8sApp:
        if isinstance(k8s_object, V1Deployment):
            return K8sAppDeployment(k8s_object)
        elif isinstance(k8s_object, V1StatefulSet):
            return K8sAppStatefulSet(k8s_object)
        elif isinstance(k8s_object, V1beta1CronJob):
            return K8sAppCronJob(k8s_object)
        else:
            raise ValueError(k8s_object)

    @staticmethod
    def get_app_container(
        spec: V1PodSpec | None, ignore_containers: Set[str] = set()
    ) -> Optional[V1Container]:
        if spec and spec.containers:
            for container in spec.containers:
                if container.name not in ignore_containers:
                    return container
        return None

    @staticmethod
    def get_ignore_containers() -> Set[str]:
        return {container["name"] for container in settings.k8s.containers.ignore}

    @staticmethod
    def get_labels() -> Set[str]:
        return set(settings.k8s.labels)


class K8sAppCronJob(K8sApp):
    def __init__(self, k8s_object: V1beta1CronJob):
        super().__init__(k8s_object)

    def setup(self):
        self.spec = self._get_pod_spec()
        self.container = self.get_app_container(self.spec)
        self.extract_config()
        self.__get_attributes()

    def _get_pod_spec(self) -> V1PodSpec | None:
        if (
            self.k8s_object.spec
            and self.k8s_object.spec.job_template.spec
            and self.k8s_object.spec.job_template.spec.template.spec
        ):
            return self.k8s_object.spec.job_template.spec.template.spec

    def __get_attributes(self):
        labels = self.metadata.labels or {}
        labels_to_use = self.get_labels()

        for key in labels_to_use:
            value = labels.get(key)
            if value is not None:
                self.attributes[key] = value
            elif self.is_streams_bootstrap_app():
                logger.warning(
                    f"{self.class_name} {self.name} does not have a label with the name: {key}"
                )

        pipeline = self.get_pipeline()
        if pipeline is not None:
            self.attributes[ATTR_PIPELINE] = pipeline


class K8sAppDeployment(K8sApp):
    def __init__(self, k8s_object: V1Deployment):
        super().__init__(k8s_object)


class K8sAppStatefulSet(K8sApp):
    def __init__(self, k8s_object: V1StatefulSet):
        super().__init__(k8s_object)

    def get_service_name(self) -> str | None:
        if self.k8s_object.spec:
            return self.k8s_object.spec.service_name
