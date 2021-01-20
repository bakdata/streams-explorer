from dynaconf import Dynaconf, Validator

APP_NAME = "Streams Explorer"
API_PREFIX = "/api"

settings = Dynaconf(
    envvar_prefix="se",
    settings_files=["settings.yaml"],
    load_dotenv=True,
    validators=[
        Validator("kafkaconnect.url", must_exist=True),
        Validator(
            "kafkaconnect.displayed_information", must_exist=True, is_type_of=list
        ),
        Validator("k8s.deployment.cluster", must_exist=True, is_type_of=bool),
        Validator("k8s.deployment.context", is_type_of=str),
        Validator("k8s.deployment.namespaces", must_exist=True, is_type_of=list),
        Validator("k8s.containers.ignore", is_type_of=list),
        Validator("k8s.labels", must_exist=True, is_type_of=list),
        Validator("k8s.independent_graph", must_exist=True, is_type_of=dict),
        Validator("schemaregistry.url", must_exist=True, is_type_of=str),
        Validator("prometheus.url", must_exist=True, is_type_of=str),
        Validator("plugins.path", must_exist=True, is_type_of=str),
        Validator("plugins.extractors.default", must_exist=True, is_type_of=bool),
    ],
)
