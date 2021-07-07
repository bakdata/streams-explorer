from dynaconf import Dynaconf, Validator

APP_NAME = "Streams Explorer"
API_PREFIX = "/api"

settings = Dynaconf(
    envvar_prefix="se",
    settings_files=["settings.yaml"],
    load_dotenv=True,
    validators=[
        Validator("graph.update_interval", must_exist=True, is_type_of=int),
        Validator("graph.layout_arguments", must_exist=True, is_type_of=str),
        Validator("graph.pipeline_distance", must_exist=True, is_type_of=int),
        Validator("k8s.deployment.cluster", must_exist=True, is_type_of=bool),
        Validator("k8s.deployment.context", is_type_of=str),
        Validator("k8s.deployment.namespaces", must_exist=True, is_type_of=list),
        Validator("k8s.containers.ignore", is_type_of=list),
        Validator("k8s.labels", must_exist=True, is_type_of=list),
        Validator("k8s.pipeline.label", must_exist=True, is_type_of=str),
        Validator("k8s.consumer_group_annotation", must_exist=True, is_type_of=str),
        Validator("kafkaconnect.url", default=None),
        Validator("kafkaconnect.displayed_information", is_type_of=list, default=[]),
        Validator("schemaregistry.url", default=None),
        Validator("prometheus.url", must_exist=True, is_type_of=str),
        Validator("grafana.dashboards.topics", is_type_of=str),
        Validator("grafana.dashboards.consumergroups", is_type_of=str),
        Validator("akhq.enable", is_type_of=bool),
        Validator("kowl.enable", is_type_of=bool),
        Validator("akhq.enable", eq=False) | Validator("kowl.enable", eq=False),
        Validator("kibanalogs.enable", is_type_of=bool),
        Validator("loki.enable", is_type_of=bool),
        Validator("kibanalogs.enable", eq=False) | Validator("loki.enable", eq=False),
        Validator("plugins.path", must_exist=True, is_type_of=str),
        Validator("plugins.extractors.default", must_exist=True, is_type_of=bool),
    ],
)
