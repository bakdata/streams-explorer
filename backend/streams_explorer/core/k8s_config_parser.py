from __future__ import annotations

from typing import TYPE_CHECKING

from streams_explorer.models.k8s_config import K8sConfig

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sApp


class K8sConfigParser:
    def __init__(self, k8s_app: K8sApp):
        self.k8s_app = k8s_app

    def parse(self) -> K8sConfig:
        ...

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


class K8sConfigParserEnv(K8sConfigParser):
    # TODO: probably this is not needed
    def __init__(self, k8s_app: K8sApp):
        super().__init__(k8s_app)

    def parse(self) -> K8sConfig:
        container = self.k8s_app.container

        if not container:
            raise ValueError("no container")  # TODO

        config = K8sConfig()
        if not container.env:
            return config

        for env in container.env:
            if env.name == self._get_env_name("INPUT_TOPICS"):
                config.input_topics = self.parse_input_topics(env.value)
            elif env.name == self._get_env_name("OUTPUT_TOPIC"):
                config.output_topic = env.value
            elif env.name == self._get_env_name("ERROR_TOPIC"):
                config.error_topic = env.value
            elif env.name == self._get_env_name("EXTRA_INPUT_TOPICS"):
                config.extra_input_topics = self.parse_extra_topics(env.value)
            elif env.name == self._get_env_name("EXTRA_OUTPUT_TOPICS"):
                config.extra_output_topics = self.parse_extra_topics(env.value)
            else:
                config.extra[env.name] = env.value
        return config

    def _get_env_name(self, variable_name: str) -> str:
        return f"{self.k8s_app.env_prefix}{variable_name}"


class K8sConfigParserArgs(K8sConfigParser):
    def __init__(self, k8s_app: K8sApp):
        super().__init__(k8s_app)

    def parse(self) -> K8sConfig:
        container = self.k8s_app.container
        if not container:
            raise ValueError("no container")

        config = K8sConfig()
        if not container.args:
            return config
        args: list[str] = container.args

        for arg in args:
            arg = self.__remove_prefix(arg)
            name, value = arg.split("=")
            if not name or not value:
                continue
            if name == "input-topics":
                config.input_topics = self.parse_input_topics(value)
            elif name == "output-topic":
                config.output_topic = value
            elif name == "error-topic":
                config.error_topic = value
            elif name == "extra-input-topics":
                config.extra_input_topics = self.parse_extra_topics(value)
            elif name == "extra-output-topics":
                config.extra_output_topics = self.parse_extra_topics(value)
            else:
                name = self.__normalise_name(name)
                config.extra[name] = value
        return config

    @staticmethod
    def __normalise_name(name: str) -> str:
        return name.upper().replace("-", "_")

    @staticmethod
    def __remove_prefix(name: str, prefix: str = "-") -> str:
        return name.lstrip(prefix)
