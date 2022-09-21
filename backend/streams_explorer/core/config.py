from typing import Any, TypeAlias

from dynaconf import Dynaconf, Validator

APP_NAME = "Streams Explorer"
API_PREFIX = "/api"

settings: Any = Dynaconf(
    envvar_prefix="se",
    settings_files=["settings.yaml"],
    load_dotenv=True,
    validators=[
        Validator("graph.update_interval", must_exist=True, is_type_of=int),
        Validator("graph.layout_arguments", must_exist=True, is_type_of=str),
        Validator("graph.pipeline_distance", must_exist=True, is_type_of=int),
        Validator(
            "graph.resolve.input_pattern_topics.all", must_exist=True, is_type_of=bool
        ),
        Validator(
            "graph.resolve.input_pattern_topics.pipelines",
            must_exist=True,
            is_type_of=bool,
        ),
        Validator("k8s.deployment.cluster", must_exist=True, is_type_of=bool),
        Validator("k8s.deployment.context", is_type_of=str),
        Validator("k8s.deployment.namespaces", must_exist=True, is_type_of=list),
        Validator("k8s.containers.ignore", is_type_of=list),
        Validator("k8s.labels", must_exist=True, is_type_of=list),
        Validator("k8s.pipeline.label", must_exist=True, is_type_of=str),
        Validator("k8s.consumer_group_annotation", must_exist=True, is_type_of=str),
        Validator("kafka.enable", eq=False, default=False)
        | (
            Validator("kafka.enable", eq=True)
            & Validator(
                "kafka.config",
                is_type_of=dict,
                must_exist=True,
                condition=lambda v: type(v.get("bootstrap.servers")) is str,
            )
        ),
        Validator("kafka.displayed_information", is_type_of=list, default=[]),
        Validator("kafka.topic_names_cache.ttl", is_type_of=int, default=3600),
        Validator("node_info.cache_ttl", must_exist=True, is_type_of=int),
        Validator("kafkaconnect.url", default=None),
        Validator("kafkaconnect.update_interval", is_type_of=int, default=300),
        Validator("kafkaconnect.displayed_information", is_type_of=list, default=[]),
        Validator("schemaregistry.url", default=None),
        Validator("prometheus.url", must_exist=True, is_type_of=str),
        Validator("grafana.enable", is_type_of=bool, default=False),
        Validator("grafana.dashboards.topics", is_type_of=str),
        Validator("grafana.dashboards.consumergroups", is_type_of=str),
        Validator("akhq.enable", is_type_of=bool, default=False),
        Validator("redpanda_console.enable", is_type_of=bool, default=False),
        Validator("akhq.enable", eq=False)
        | Validator("redpanda_console.enable", eq=False),
        Validator("kibanalogs.enable", is_type_of=bool, default=False),
        Validator("loki.enable", is_type_of=bool, default=False),
        Validator("kibanalogs.enable", eq=False) | Validator("loki.enable", eq=False),
        Validator("plugins.path", must_exist=True, is_type_of=str),
        Validator("plugins.extractors.default", must_exist=True, is_type_of=bool),
    ],
)

InfoList: TypeAlias = list[dict[str, str]]


def sort_displayed_information(lst: InfoList) -> InfoList:
    return sorted(lst, key=lambda k: str.casefold(k["name"]))


settings.k8s.displayed_information = sort_displayed_information(
    settings.k8s.displayed_information
)
settings.kafka.displayed_information = sort_displayed_information(
    settings.kafka.displayed_information
)
settings.kafkaconnect.displayed_information = sort_displayed_information(
    settings.kafkaconnect.displayed_information
)
