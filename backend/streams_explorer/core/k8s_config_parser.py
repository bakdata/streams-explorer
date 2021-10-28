from __future__ import annotations

from typing import TYPE_CHECKING

from kubernetes.client import V1Container

from streams_explorer.models.k8s_config import K8sConfig

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sApp


class K8sConfigParser:
    """Base class for parsing configuration of streaming application deployments."""

    def __init__(self, k8s_app: K8sApp):
        self.k8s_app = k8s_app

    def parse(self) -> K8sConfig:
        ...


class StreamsBootstrapConfigParser(K8sConfigParser):
    """Config parser for deployments configured through streams-bootstrap."""

    def __init__(self, k8s_app: K8sApp):
        super().__init__(k8s_app)
        self._id = self.get_id()
        self.config = K8sConfig(self._id, name=self.get_name())

    def get_id(self) -> str:
        name = None
        if self.k8s_app.metadata.labels:
            name = self.k8s_app.metadata.labels.get("app")
        if not name:
            name = self.k8s_app.metadata.name
        if not name:
            raise TypeError(f"Name is required for {self.k8s_app.get_class_name()}")
        return name

    def get_name(self) -> str:
        return self._id

    def parse_config(self, name: str, value: str):
        if name == "INPUT_TOPICS":
            self.config.input_topics = self.parse_input_topics(value)
        elif name == "OUTPUT_TOPIC":
            self.config.output_topic = value
        elif name == "ERROR_TOPIC":
            self.config.error_topic = value
        elif name == "EXTRA_INPUT_TOPICS":
            self.config.extra_input_topics = self.parse_extra_topics(value)
        elif name == "EXTRA_OUTPUT_TOPICS":
            self.config.extra_output_topics = self.parse_extra_topics(value)
        else:
            self.config.extra[name] = value

    @staticmethod
    def parse_input_topics(input_topics: str) -> list[str]:
        return input_topics.split(",")

    @staticmethod
    def parse_extra_topics(extra_topics: str) -> list[str]:
        # remove trailing commas
        extra_topics = extra_topics[:-1] if extra_topics[-1] == "," else extra_topics
        return list(
            map(
                lambda topic: topic.split("=")[1],
                extra_topics.split(","),
            )
        )

    @staticmethod
    def remove_prefix(name: str, prefix: str) -> str:
        if name.startswith(prefix):
            initial = len(prefix)
            return name[initial:]
        return name


class StreamsBootstrapEnvParser(StreamsBootstrapConfigParser):
    """Default parser for streams-bootstrap deployments configured through environment variables."""

    def __init__(self, k8s_app: K8sApp):
        super().__init__(k8s_app)
        self.env_prefix = self.get_env_prefix(self.k8s_app.container)

    def parse(self) -> K8sConfig:
        container = self.k8s_app.container

        if not container or not container.env:
            return self.config

        for env in container.env:
            if env.value is not None:
                name = self.__normalise_name(env.name)
                self.parse_config(name, env.value)
        return self.config

    def __normalise_name(self, name: str) -> str:
        if self.env_prefix:
            return self.remove_prefix(name, self.env_prefix)
        return name

    @staticmethod
    def get_env_prefix(container: V1Container | None) -> str | None:
        if container and container.env:
            for env_var in container.env:
                if env_var.name == "ENV_PREFIX":
                    return env_var.value
        return None


class StreamsBootstrapArgsParser(StreamsBootstrapConfigParser):
    """Optional parser for streams-bootstrap deployments configured through CLI arguments."""

    def parse(self) -> K8sConfig:
        container = self.k8s_app.container

        if not container or not container.args:
            return self.config

        args: list[str] = container.args

        for arg in args:
            arg = self.remove_prefix(arg, "--")
            name, value = arg.split("=")
            if not name or not value:
                continue
            name = self.__normalise_name(name)
            self.parse_config(name, value)
        return self.config

    @staticmethod
    def __normalise_name(name: str) -> str:
        return name.upper().replace("-", "_")
