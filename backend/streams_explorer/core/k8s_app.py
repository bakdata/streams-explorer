from typing import Dict, List, Optional, Set

from kubernetes.client import (
    V1beta1CronJob,
    V1Container,
    V1Deployment,
    V1ObjectMeta,
    V1PodSpec,
)
from kubernetes.client.models.v1_stateful_set import V1StatefulSet
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.extractors import extractor_container


class K8sApp:
    def __init__(self, k8s_object):
        self.k8s_object = k8s_object
        self.metadata: Optional[V1ObjectMeta] = k8s_object.metadata
        self.name = self.get_name()
        self.input_topics: List[str] = []
        self.output_topic: Optional[str] = None
        self.error_topic: Optional[str] = None
        self.extra_input_topics: List[str] = []
        self.extra_output_topics: List[str] = []
        self.attributes: Dict[str, str] = {}

    def to_dict(self) -> dict:
        return self.k8s_object.to_dict()

    def get_name(self) -> str:
        name = self.metadata.labels.get("app")
        if not name:
            raise TypeError(f"Name is required for {self.__class__.__name__}")
        return name

    def get_common_configuration(self):
        for env in self.container.env:
            name = env.name
            if name == self.get_env_name("INPUT_TOPICS"):
                self.input_topics = self.parse_input_topics(env.value)
            elif name == self.get_env_name("OUTPUT_TOPIC"):
                self.output_topic = env.value
            elif name == self.get_env_name("ERROR_TOPIC"):
                self.error_topic = env.value
            elif name == self.get_env_name("EXTRA_INPUT_TOPICS"):
                self.extra_input_topics = self.parse_extra_topics(env.value)
            elif name == self.get_env_name("EXTRA_OUTPUT_TOPICS"):
                self.extra_output_topics = self.parse_extra_topics(env.value)

            if self.name:
                extractor_container.on_streaming_app_env_parsing(env, self.name)

    def is_common_streams_app(self) -> bool:
        if self.input_topics is None and self.output_topic is None:
            return False
        return True

    def get_env_name(self, variable_name) -> str:
        return f"{self.env_prefix}{variable_name}"

    def get_attributes(self):
        labels = self.metadata.labels
        labels_to_use = self.get_labels()

        for key in labels_to_use:
            value = labels.get(key)
            if value is not None:
                self.attributes[key] = value
            elif self.is_common_streams_app():
                logger.warning(
                    f"{self.__class__.__name__} {self.name} does not have a label with the name: {key}"
                )

        if (
            self.k8s_object.spec.template.metadata
            and self.k8s_object.spec.template.metadata.annotations
        ):
            annotations = self.k8s_object.spec.template.metadata.annotations
            self.attributes.update(annotations)

    @staticmethod
    def get_env_prefix(container: Optional[V1Container]) -> Optional[str]:
        if container:
            for env_var in container.env:
                if env_var.name == "ENV_PREFIX":
                    return env_var.value
        return None

    @staticmethod
    def get_app_container(
        spec: V1PodSpec, ignore_containers: Set[str] = set()
    ) -> Optional[V1Container]:
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

    @staticmethod
    def parse_input_topics(input_topics: str) -> List[str]:
        return input_topics.split(",")

    @staticmethod
    def parse_extra_topics(extra_topics: str) -> List[str]:
        # remove trailing commas
        extra_topics = extra_topics[:-1] if extra_topics[-1] == "," else extra_topics
        return list(
            map(
                lambda topic: topic.split("=")[1],
                extra_topics.split(","),
            )
        )


class K8sAppCronJob(K8sApp):
    def __init__(self, k8s_object: V1beta1CronJob):
        super().__init__(k8s_object)
        self.spec = self.k8s_object.spec.job_template.spec.template.spec
        self.container = self.get_app_container(self.spec)
        self.env_prefix = self.get_env_prefix(self.container)

        self.get_common_configuration()

    def get_name(self) -> str:
        name = self.metadata.name
        if not name:
            raise TypeError(f"Name is required for {self.__class__.__name__}")
        return name

    def get_common_configuration(self):
        for env in self.container.env:
            name = env.name
            if name == self.get_env_name("INPUT_TOPICS"):
                self.input_topics = self.parse_input_topics(env.value)
            elif name == self.get_env_name("OUTPUT_TOPIC"):
                self.output_topic = env.value
            elif name == self.get_env_name("ERROR_TOPIC"):
                self.error_topic = env.value


class K8sAppDeployment(K8sApp):
    def __init__(self, k8s_object: V1Deployment):
        super().__init__(k8s_object)
        self.spec = self.k8s_object.spec.template.spec
        self._ignore_containers = self.get_ignore_containers()
        self.container = self.get_app_container(self.spec, self._ignore_containers)
        self.env_prefix = self.get_env_prefix(self.container)

        self.get_common_configuration()
        self.get_attributes()


class K8sAppStatefulSet(K8sApp):
    def __init__(self, k8s_object: V1StatefulSet):
        super().__init__(k8s_object)
        self.spec = self.k8s_object.spec.template.spec
        self._ignore_containers = self.get_ignore_containers()
        self.container = self.get_app_container(self.spec, self._ignore_containers)
        self.env_prefix = self.get_env_prefix(self.container)

        self.get_common_configuration()
        self.get_attributes()
