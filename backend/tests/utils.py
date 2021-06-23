from typing import List

from kubernetes.client import (
    V1beta1CronJob,
    V1beta1CronJobSpec,
    V1beta1JobTemplateSpec,
    V1Container,
    V1Deployment,
    V1DeploymentSpec,
    V1EnvVar,
    V1JobSpec,
    V1ObjectMeta,
    V1PodSpec,
    V1PodTemplateSpec,
    V1StatefulSet,
    V1StatefulSetSpec,
)

from streams_explorer.core.k8s_app import ATTR_PIPELINE


def get_streaming_app_deployment(
    name="test-app",
    input_topics="input-topic",
    output_topic="output-topic",
    error_topic="error-topic",
    multiple_inputs=None,
    multiple_outputs=None,
    env_prefix="APP_",
    pipeline=None,
    consumer_group=None,
) -> V1Deployment:
    template = get_template(
        input_topics,
        output_topic,
        error_topic,
        multiple_inputs=multiple_inputs,
        multiple_outputs=multiple_outputs,
        env_prefix=env_prefix,
        consumer_group=consumer_group,
    )
    spec = V1DeploymentSpec(
        template=template, selector="app=test-app,release=test-release"
    )
    metadata = get_metadata(name, pipeline=pipeline)
    return V1Deployment(metadata=metadata, spec=spec)


def get_streaming_app_stateful_set(
    name="test-app",
    input_topics="input-topic",
    output_topic="output-topic",
    error_topic="error-topic",
    multiple_inputs=None,
    multiple_outputs=None,
    env_prefix="APP_",
    pipeline=None,
    consumer_group=None,
    service_name="test-service",
) -> V1StatefulSet:
    template = get_template(
        input_topics,
        output_topic,
        error_topic,
        multiple_inputs=multiple_inputs,
        multiple_outputs=multiple_outputs,
        env_prefix=env_prefix,
        consumer_group=consumer_group,
    )
    metadata = get_metadata(name, pipeline=pipeline)
    spec = V1StatefulSetSpec(
        service_name=service_name,
        template=template,
        selector="app=test-app,release=test-release",
    )

    return V1StatefulSet(metadata=metadata, spec=spec)


def get_streaming_app_cronjob(
    name="test-cronjob",
    input_topics="",
    output_topic="output-topic",
    error_topic="error-topic",
    env_prefix="APP_",
    pipeline=None,
) -> V1beta1CronJob:
    env = get_env(
        input_topics,
        output_topic,
        error_topic,
        env_prefix=env_prefix,
    )
    container = V1Container(name="test-container", env=env)
    pod_spec = V1PodSpec(containers=[container])
    pod_template_spec = V1PodTemplateSpec(spec=pod_spec)
    job_spec = V1JobSpec(
        template=pod_template_spec,
        selector="",
    )
    job_template = V1beta1JobTemplateSpec(spec=job_spec)
    spec = V1beta1CronJobSpec(job_template=job_template, schedule="* * * * *")
    metadata = get_metadata(name, pipeline=pipeline)
    return V1beta1CronJob(metadata=metadata, spec=spec)


def get_metadata(name, pipeline=None) -> V1ObjectMeta:
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
        namespace="test-namespace",
    )


def get_env(
    input_topics,
    output_topic,
    error_topic,
    multiple_inputs=None,
    multiple_outputs=None,
    env_prefix="APP_",
) -> List[V1EnvVar]:
    env = [
        V1EnvVar(name="ENV_PREFIX", value=env_prefix),
        V1EnvVar(name=env_prefix + "OUTPUT_TOPIC", value=output_topic),
        V1EnvVar(name=env_prefix + "ERROR_TOPIC", value=error_topic),
    ]
    if input_topics:
        env.append(V1EnvVar(name=env_prefix + "INPUT_TOPICS", value=input_topics))
    if multiple_inputs:
        env.append(
            V1EnvVar(name=env_prefix + "EXTRA_INPUT_TOPICS", value=multiple_inputs)
        )
    if multiple_outputs:
        env.append(
            V1EnvVar(name=env_prefix + "EXTRA_OUTPUT_TOPICS", value=multiple_outputs)
        )
    return env


def get_template(
    input_topics,
    output_topic,
    error_topic,
    multiple_inputs=None,
    multiple_outputs=None,
    env_prefix="APP_",
    consumer_group=None,
) -> V1PodTemplateSpec:
    env = get_env(
        input_topics,
        output_topic,
        error_topic,
        multiple_inputs,
        multiple_outputs,
        env_prefix,
    )
    container = V1Container(name="test-container", env=env)
    pod_spec = V1PodSpec(containers=[container])
    spec_metadata = None
    if consumer_group is not None:
        spec_metadata = V1ObjectMeta(
            annotations={"consumerGroup": consumer_group},
        )
    return V1PodTemplateSpec(spec=pod_spec, metadata=spec_metadata)
