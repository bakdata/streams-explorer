from __future__ import annotations

from typing import TYPE_CHECKING

from streams_explorer.models.k8s_config import K8sConfig

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sApp


class K8sConfigParser:
    def __init__(self, k8s_app: K8sApp):
        self.k8s_app = k8s_app
        self.config = K8sConfig()

    def parse(self) -> K8sConfig:
        ...

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


class K8sConfigParserEnv(K8sConfigParser):
    # TODO: probably not needed here
    def __init__(self, k8s_app: K8sApp):
        super().__init__(k8s_app)

    def parse(self) -> K8sConfig:
        container = self.k8s_app.container

        if not container:
            raise ValueError("no container")  # TODO

        if not container.env:
            return self.config

        for env in container.env:
            name = self.__normalise_name(env.name)
            self.parse_config(name, env.value)
        return self.config

    def __normalise_name(self, name: str) -> str:
        if self.k8s_app.env_prefix:
            return self.remove_prefix(name, self.k8s_app.env_prefix)
        return name


class K8sConfigParserArgs(K8sConfigParser):
    def __init__(self, k8s_app: K8sApp):
        super().__init__(k8s_app)

    def parse(self) -> K8sConfig:
        container = self.k8s_app.container
        if not container:
            raise ValueError("no container")

        if not container.args:
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
