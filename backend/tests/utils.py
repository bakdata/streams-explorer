from enum import Enum
from typing import Literal

from kubernetes_asyncio.client import (
    V1Container,
    V1CronJob,
    V1CronJobSpec,
    V1Deployment,
    V1DeploymentSpec,
    V1DeploymentStatus,
    V1EnvVar,
    V1JobSpec,
    V1JobTemplateSpec,
    V1LabelSelector,
    V1ObjectMeta,
    V1PodSpec,
    V1PodTemplateSpec,
    V1StatefulSet,
    V1StatefulSetSpec,
)

from streams_explorer.core.k8s_app import ATTR_PIPELINE


class ConfigType(str, Enum):
    ENV = "env"
    ARGS = "args"


StreamsBootstrapVersion = Literal[2, 3]


def get_streaming_app_deployment(
    name: str = "test-app",
    input_topics: str | None = "input-topic",
    output_topic: str | None = "output-topic",
    error_topic: str | None = "error-topic",
    input_pattern: str | None = None,
    multiple_inputs: str | None = None,
    multiple_outputs: str | None = None,
    labeled_input_patterns: str | None = None,
    extra: dict[str, str] = {},
    env_prefix: str = "APP_",
    namespace: str = "test-namespace",
    pipeline: str | None = None,
    consumer_group: str | None = None,
    config_type: ConfigType = ConfigType.ENV,
    streams_bootstrap_version: StreamsBootstrapVersion = 3,
) -> V1Deployment:
    template = get_template(
        input_topics=input_topics,
        output_topic=output_topic,
        error_topic=error_topic,
        input_pattern=input_pattern,
        multiple_inputs=multiple_inputs,
        multiple_outputs=multiple_outputs,
        labeled_input_patterns=labeled_input_patterns,
        extra=extra,
        env_prefix=env_prefix,
        consumer_group=consumer_group,
        config_type=config_type,
        streams_bootstrap_version=streams_bootstrap_version,
    )
    spec = V1DeploymentSpec(template=template, selector=V1LabelSelector())
    metadata = get_metadata(name, namespace=namespace, pipeline=pipeline)
    status = V1DeploymentStatus(ready_replicas=None, replicas=1)
    return V1Deployment(metadata=metadata, spec=spec, status=status)


def get_streaming_app_stateful_set(
    name: str = "test-app",
    input_topics: str = "input-topic",
    output_topic: str = "output-topic",
    error_topic: str = "error-topic",
    input_pattern: str | None = None,
    multiple_inputs: str | None = None,
    multiple_outputs: str | None = None,
    labeled_input_patterns: str | None = None,
    extra: dict[str, str] = {},
    env_prefix: str = "APP_",
    namespace: str = "test-namespace",
    pipeline: str | None = None,
    consumer_group: str | None = None,
    service_name: str = "test-service",
    config_type: ConfigType = ConfigType.ENV,
    streams_bootstrap_version: StreamsBootstrapVersion = 3,
) -> V1StatefulSet:
    template = get_template(
        input_topics=input_topics,
        output_topic=output_topic,
        error_topic=error_topic,
        input_pattern=input_pattern,
        multiple_inputs=multiple_inputs,
        multiple_outputs=multiple_outputs,
        labeled_input_patterns=labeled_input_patterns,
        extra=extra,
        env_prefix=env_prefix,
        consumer_group=consumer_group,
        config_type=config_type,
        streams_bootstrap_version=streams_bootstrap_version,
    )
    metadata = get_metadata(name, namespace=namespace, pipeline=pipeline)
    spec = V1StatefulSetSpec(
        service_name=service_name,
        template=template,
        selector=V1LabelSelector(),
    )

    return V1StatefulSet(metadata=metadata, spec=spec)


def get_streaming_app_cronjob(
    name: str = "test-cronjob",
    input_topics: str | None = None,
    output_topic: str | None = "output-topic",
    error_topic: str | None = "error-topic",
    env_prefix: str = "APP_",
    namespace: str = "test-namespace",
    pipeline: str | None = None,
    streams_bootstrap_version: StreamsBootstrapVersion = 3,
) -> V1CronJob:
    env = get_env(
        input_topics=input_topics,
        output_topic=output_topic,
        error_topic=error_topic,
        env_prefix=env_prefix,
        streams_bootstrap_version=streams_bootstrap_version,
    )
    container = V1Container(name="test-container", env=env)
    pod_spec = V1PodSpec(containers=[container])
    pod_template_spec = V1PodTemplateSpec(spec=pod_spec)
    job_spec = V1JobSpec(
        template=pod_template_spec,
        selector=None,
    )
    job_template = V1JobTemplateSpec(spec=job_spec)
    spec = V1CronJobSpec(job_template=job_template, schedule="* * * * *")
    metadata = get_metadata(name, namespace=namespace, pipeline=pipeline)
    return V1CronJob(metadata=metadata, spec=spec)


def get_metadata(name, *, namespace: str, pipeline: str | None = None) -> V1ObjectMeta:
    return V1ObjectMeta(
        annotations={
            "deployment.kubernetes.io/revision": "1",
        },
        labels={
            "app": name,
            "app_name": "test-app-name",
            "chart": "streams-app-0.1.0",
            "release": "test-release",
            ATTR_PIPELINE: pipeline,
        },
        name=name,
        namespace=namespace,
    )


def get_env(
    *,
    input_topics: str | None,
    output_topic: str | None,
    error_topic: str | None,
    input_pattern: str | None = None,
    multiple_inputs: str | None = None,
    multiple_outputs: str | None = None,
    labeled_input_patterns: str | None = None,
    extra: dict[str, str] = {},
    env_prefix: str,
    streams_bootstrap_version: StreamsBootstrapVersion,
) -> list[V1EnvVar]:
    labeled_topics_prefix = "EXTRA" if streams_bootstrap_version == 2 else "LABELED"
    env = [V1EnvVar(name="ENV_PREFIX", value=env_prefix)]
    if input_topics:
        env.append(V1EnvVar(name=env_prefix + "INPUT_TOPICS", value=input_topics))
    if output_topic:
        env.append(V1EnvVar(name=env_prefix + "OUTPUT_TOPIC", value=output_topic))
    if error_topic:
        env.append(V1EnvVar(name=env_prefix + "ERROR_TOPIC", value=error_topic))
    if input_pattern:
        env.append(V1EnvVar(name=env_prefix + "INPUT_PATTERN", value=input_pattern))
    if multiple_inputs:
        env.append(
            V1EnvVar(
                name=env_prefix + labeled_topics_prefix + "_INPUT_TOPICS",
                value=multiple_inputs,
            )
        )
    if multiple_outputs:
        env.append(
            V1EnvVar(
                name=env_prefix + labeled_topics_prefix + "_OUTPUT_TOPICS",
                value=multiple_outputs,
            )
        )
    if labeled_input_patterns:
        env.append(
            V1EnvVar(
                name=env_prefix + labeled_topics_prefix + "_INPUT_PATTERNS",
                value=labeled_input_patterns,
            )
        )
    if extra:
        for k, v in extra.items():
            env.append(V1EnvVar(name=env_prefix + k, value=v))
    return env


def _create_arg(name: str, value: str) -> str:
    return f"--{name}={value}"


def get_args(
    *,
    input_topics: str | None,
    output_topic: str | None,
    error_topic: str | None,
    multiple_inputs: str | None,
    multiple_outputs: str | None,
    labeled_input_patterns: str | None,
    extra: dict[str, str],
    streams_bootstrap_version: StreamsBootstrapVersion,
) -> list[str]:
    args = []
    if input_topics:
        args.append(_create_arg("input-topics", input_topics))
    if output_topic:
        args.append(_create_arg("output-topic", output_topic))
    if error_topic:
        args.append(_create_arg("error-topic", error_topic))
    if multiple_inputs:
        args.append(_create_arg("extra-input-topics", multiple_inputs))
    if multiple_outputs:
        args.append(_create_arg("extra-output-topics", multiple_outputs))
    if labeled_input_patterns:
        args.append(_create_arg("extra-input-patterns", labeled_input_patterns))
    if extra:
        for k, v in extra.items():
            args.append(_create_arg(k, v))
    return args


def get_template(
    *,
    input_topics: str | None,
    output_topic: str | None,
    error_topic: str | None,
    input_pattern: str | None,
    multiple_inputs: str | None,
    multiple_outputs: str | None,
    labeled_input_patterns: str | None,
    extra: dict[str, str],
    env_prefix: str,
    consumer_group: str | None,
    config_type: ConfigType,
    streams_bootstrap_version: StreamsBootstrapVersion,
) -> V1PodTemplateSpec:
    env = None
    args = None
    match config_type:
        case ConfigType.ENV:
            env = get_env(
                input_topics=input_topics,
                output_topic=output_topic,
                error_topic=error_topic,
                input_pattern=input_pattern,
                multiple_inputs=multiple_inputs,
                multiple_outputs=multiple_outputs,
                labeled_input_patterns=labeled_input_patterns,
                env_prefix=env_prefix,
                extra=extra,
                streams_bootstrap_version=streams_bootstrap_version,
            )
        case ConfigType.ARGS:
            args = get_args(
                input_topics=input_topics,
                output_topic=output_topic,
                error_topic=error_topic,
                multiple_inputs=multiple_inputs,
                multiple_outputs=multiple_outputs,
                labeled_input_patterns=labeled_input_patterns,
                extra=extra,
                streams_bootstrap_version=streams_bootstrap_version,
            )
    container = V1Container(name="test-container", env=env, args=args)
    pod_spec = V1PodSpec(containers=[container])
    spec_metadata = None
    if consumer_group is not None:
        spec_metadata = V1ObjectMeta(
            annotations={"consumerGroup": consumer_group},
        )
    return V1PodTemplateSpec(spec=pod_spec, metadata=spec_metadata)
