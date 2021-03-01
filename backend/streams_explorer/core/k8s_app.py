from typing import Dict, List, Optional, Set

from kubernetes.client import (
    V1beta1CronJob,
    V1Container,
    V1Deployment,
    V1ObjectMeta,
    V1PodSpec,
)
from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.extractors import extractor_container


class K8sApp:
    def __init__(self):
        self.name = None
        self.metadata = None
        self.input_topics = None
        self.output_topic = None
        self.error_topic = None
        self.extra_input_topics = None
        self.extra_output_topics = None
        self.attributes: Dict[str, str] = {}

    def to_dict(self) -> dict:
        pass

    def get_name(self) -> Optional[str]:
        pass

    @staticmethod
    def get_env_prefix(container: V1Container) -> Optional[str]:
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


class K8sAppCronJob(K8sApp):
    def __init__(self, cron_job: V1beta1CronJob):
        super().__init__()
        self.cron_job = cron_job
        self.metadata: V1ObjectMeta = cron_job.metadata
        self.name = self.get_name()
        self.spec = cron_job.spec.job_template.spec.template.spec
        self.container = self.get_app_container(self.spec)
        self._env_prefix = self.get_env_prefix(self.container)

        self.__get_common_configuration()

    def get_name(self) -> Optional[str]:
        return self.metadata.name

    def _get_env_name(self, variable_name) -> str:
        return f"{self._env_prefix}{variable_name}"

    def __get_common_configuration(self):
        for env in self.container.env:
            name = env.name
            if name == self._get_env_name("INPUT_TOPICS"):
                self.input_topics = self.parse_input_topics(env.value)
            elif name == self._get_env_name("OUTPUT_TOPIC"):
                self.output_topic = env.value
            elif name == self._get_env_name("ERROR_TOPIC"):
                self.error_topic = env.value


class K8sAppDeployment(K8sApp):
    def __init__(self, deployment: V1Deployment):
        super().__init__()
        self.deployment = deployment
        self.metadata: V1ObjectMeta = deployment.metadata
        self.name = self.get_name()
        self.spec = deployment.spec.template.spec
        self._ignore_containers = self.get_ignore_containers()
        self.container = self.get_app_container(self.spec, self._ignore_containers)
        self._env_prefix = self.get_env_prefix(self.container)

        self.__get_common_configuration()
        self.__get_attributes()

    def get_name(self) -> Optional[str]:
        return self.metadata.labels.get("app")

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

    def to_dict(self) -> dict:
        return self.deployment.to_dict()
