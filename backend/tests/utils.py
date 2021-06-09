from typing import List

from kubernetes.client import (
    V1Container,
    V1Deployment,
    V1DeploymentSpec,
    V1EnvVar,
    V1ObjectMeta,
    V1PodSpec,
    V1PodTemplateSpec,
    V1StatefulSet,
    V1StatefulSetSpec,
)

from streams_explorer.core.k8s_app import ATTR_PIPELINE


def get_streaming_app_deployment(
    name,
    input_topics,
    output_topic,
    error_topic,
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
    name,
    input_topics,
    output_topic,
    error_topic,
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
        name="test-app-name",
        namespace="test-namespace",
    )


def get_template(
    input_topics,
    output_topic,
    error_topic,
    multiple_inputs=None,
    multiple_outputs=None,
    env_prefix="APP_",
    consumer_group=None,
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

    container = V1Container(name="test-container", env=env)
    pod_spec = V1PodSpec(containers=[container])
    spec_metadata = None
    if consumer_group is not None:
        spec_metadata = V1ObjectMeta(
            annotations={"consumerGroup": consumer_group},
        )
    return V1PodTemplateSpec(spec=pod_spec, metadata=spec_metadata)
