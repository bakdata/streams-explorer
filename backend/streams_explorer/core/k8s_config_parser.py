from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from kubernetes_asyncio.client import V1Container

from streams_explorer.models.k8s import K8sConfig
from streams_explorer.plugins import Plugin

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sApp


class K8sConfigParser(Plugin):
    """Base class for parsing configuration of streaming application deployments."""

    def __init__(self, k8s_app: K8sApp) -> None:
        self.k8s_app = k8s_app

    @abstractmethod
    def parse(self) -> K8sConfig:
        ...

    @staticmethod
    def namespace(name: str, namespace: str | None = None) -> str:
        return f"{namespace or 'default'}/{name}"


class StreamsBootstrapConfigParser(K8sConfigParser):
    """Config parser for deployments configured through streams-bootstrap."""

    def __init__(self, k8s_app: K8sApp) -> None:
        super().__init__(k8s_app)
        self.set_id()
        self.config = K8sConfig(self._id, self._name)

    def set_id(self) -> None:
        name: str | None = None
        if self.k8s_app.metadata.labels:
            name = self.k8s_app.metadata.labels.get("app")
        if not name:
            name = self.k8s_app.metadata.name
        if not name:
            raise TypeError(f"Name is required for {self.k8s_app.class_name}")
        self._id: str = self.namespace(name, self.k8s_app.metadata.namespace)
        self._name: str = name

    def parse_config(self, name: str, value: str) -> None:
        match name:
            case "INPUT_TOPICS":
                self.config.input_topics = self.parse_input_topics(value)
            case "OUTPUT_TOPIC":
                self.config.output_topic = value
            case "ERROR_TOPIC":
                self.config.error_topic = value
            case "LABELED_INPUT_TOPICS" | "EXTRA_INPUT_TOPICS":
                self.config.labeled_input_topics = self.parse_labeled_topics(value)
            case "LABELED_OUTPUT_TOPICS" | "EXTRA_OUTPUT_TOPICS":
                self.config.labeled_output_topics = self.parse_labeled_topics(value)
            case "INPUT_PATTERN":
                self.config.input_pattern = value
            case "LABELED_INPUT_PATTERNS" | "EXTRA_INPUT_PATTERNS":
                self.config.labeled_input_patterns = self.parse_labeled_topics(value)
            case _:
                self.config.extra[name] = value

    @staticmethod
    def parse_input_topics(input_topics: str) -> list[str]:
        return input_topics.split(",")

    @staticmethod
    def parse_labeled_topics(labeled_topics: str) -> list[str]:
        labeled_topics = labeled_topics.removesuffix(",")  # remove trailing comma
        return [
            topic
            for role in labeled_topics.split(",")
            for topic in role.split("=")[1].split(";")
        ]


class StreamsBootstrapEnvParser(StreamsBootstrapConfigParser):
    """Default parser for streams-bootstrap deployments configured through environment variables."""

    def __init__(self, k8s_app: K8sApp) -> None:
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
            return name.removeprefix(self.env_prefix)
        return name

    @staticmethod
    def get_env_prefix(container: V1Container | None) -> str | None:
        if container and container.env:
            for env_var in container.env:
                if env_var.name == "ENV_PREFIX":
                    return env_var.value


class StreamsBootstrapArgsParser(StreamsBootstrapConfigParser):
    """Optional parser for streams-bootstrap deployments configured through CLI arguments."""

    def parse(self) -> K8sConfig:
        container = self.k8s_app.container

        if not container or not container.args:
            return self.config

        args: list[str] = container.args

        for arg in args:
            arg = arg.removeprefix("--")
            name, value = arg.split("=")
            if not name or not value:
                continue
            name = self.__normalise_name(name)
            self.parse_config(name, value)
        return self.config

    @staticmethod
    def __normalise_name(name: str) -> str:
        return name.upper().replace("-", "_")
