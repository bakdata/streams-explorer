from typing import Dict, List, Optional, Set

from kubernetes.client import V1Container, V1Deployment, V1ObjectMeta, V1PodSpec
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.extractors import extractor_container


class K8sApp:
    def __init__(self, deployment: V1Deployment):
        self.deployment = deployment
        self.metadata: V1ObjectMeta = deployment.metadata
        self.spec = deployment.spec.template.spec
        self._ignore_containers = self.get_ignore_containers()
        self.container = self.__get_app_container(self.spec)

        self._env_prefix = None
        self.name = None
        self.input_topics = None
        self.output_topic = None
        self.error_topic = None
        self.extra_input_topics = None
        self.extra_output_topics = None
        self.attributes: Dict[str, str] = {}

        self.get_name()
        self.get_env_prefix()
        self.__get_common_configuration()
        self.__get_attributes()

    def get_name(self):
        self.name = self.metadata.labels.get("app")

    def __get_common_configuration(self):
        for env in self.container.env:
            name = env.name
            if name == self._get_env_name("INPUT_TOPICS"):
                self.input_topics = self.parse_input_topics(env.value)
            elif name == self._get_env_name("OUTPUT_TOPIC"):
                self.output_topic = env.value
            elif name == self._get_env_name("ERROR_TOPIC"):
                self.error_topic = env.value
            elif name == self._get_env_name("EXTRA_INPUT_TOPICS"):
                self.extra_input_topics = self.parse_extra_topics(env.value)
            elif name == self._get_env_name("EXTRA_OUTPUT_TOPICS"):
                self.extra_output_topics = self.parse_extra_topics(env.value)

            extractor_container.on_streaming_app_env_parsing(env, self.name)

    def get_env_prefix(self):
        for env_var in self.container.env:
            if env_var.name == "ENV_PREFIX":
                self._env_prefix = env_var.value
                break

    def __get_attributes(self):
        labels = self.metadata.labels
        labels_to_use = self.get_labels()

        for key in labels_to_use:
            value = labels.get(key)
            if value is not None:
                self.attributes[key] = value
            elif self.is_common_streams_app():
                logger.warning(
                    f"Deployment {self.name} does not have a label with the name: {key}"
                )

        if (
            self.deployment.spec.template.metadata
            and self.deployment.spec.template.metadata.annotations
        ):
            annotations = self.deployment.spec.template.metadata.annotations
            self.attributes.update(annotations)

    def _get_env_name(self, variable_name) -> str:
        return f"{self._env_prefix}{variable_name}"

    def is_common_streams_app(self) -> bool:
        if self.input_topics is None and self.output_topic is None:
            return False
        return True

    def __get_app_container(self, spec: V1PodSpec) -> Optional[V1Container]:
        for container in spec.containers:
            if container.name not in self._ignore_containers:
                return container
        return None

    def to_dict(self) -> Dict:
        return self.deployment.to_dict()

    @staticmethod
    def get_ignore_containers() -> Set:
        return set(
            [container.get("name") for container in settings.k8s.containers.ignore]
        )

    @staticmethod
    def get_labels() -> Set:
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
