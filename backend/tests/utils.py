from kubernetes.client import (
    V1Container,
    V1Deployment,
    V1DeploymentSpec,
    V1EnvVar,
    V1ObjectMeta,
    V1PodSpec,
    V1PodTemplateSpec,
)


def get_streaming_app_deployment(
    name,
    input_topics,
    output_topic,
    error_topic,
    multiple_inputs=None,
    multiple_outputs=None,
    env_prefix="APP_",
    pipeline=None,
) -> V1Deployment:
    metadata = V1ObjectMeta(
        annotations={"deployment.kubernetes.io/revision": "1"},
        labels={
            "app": name,
            "app_name": "test-app-name",
            "chart": "streams-app-0.1.0",
            "release": "test-release",
            "pipeline": pipeline,
        },
        name="test-app-name",
        namespace="test-namespace",
    )
    envs = [
        V1EnvVar(name="ENV_PREFIX", value=env_prefix),
        V1EnvVar(name=env_prefix + "INPUT_TOPICS", value=input_topics),
        V1EnvVar(name=env_prefix + "OUTPUT_TOPIC", value=output_topic),
        V1EnvVar(name=env_prefix + "ERROR_TOPIC", value=error_topic),
    ]

    if multiple_inputs:
        envs.append(
            V1EnvVar(name=env_prefix + "EXTRA_INPUT_TOPICS", value=multiple_inputs)
        )
    if multiple_outputs:
        envs.append(
            V1EnvVar(name=env_prefix + "EXTRA_OUTPUT_TOPICS", value=multiple_outputs)
        )

    container = V1Container(name="test-container", env=envs)
    pod_spec = V1PodSpec(containers=[container])
    pod_template_spec = V1PodTemplateSpec(spec=pod_spec)
    deployment_spec = V1DeploymentSpec(
        template=pod_template_spec, selector="app=test-app,release=test-release"
    )
    return V1Deployment(metadata=metadata, spec=deployment_spec)
