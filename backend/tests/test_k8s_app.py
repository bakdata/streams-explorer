from streams_explorer.core.k8s_app import K8sApp, K8sAppDeployment, K8sAppStatefulSet
from tests.utils import get_streaming_app_deployment, get_streaming_app_stateful_set


class TestK8sApp:
    def test_init(self):
        k8s_objects = [
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic="error-topic",
            ),
            get_streaming_app_stateful_set(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic="error-topic",
            ),
        ]

        k8s_apps = [K8sApp.factory(k8s_object) for k8s_object in k8s_objects]

        for k8s_app in k8s_apps:
            assert k8s_app.name == "test-app"
            assert k8s_app.error_topic == "error-topic"
            assert k8s_app.output_topic == "output-topic"
            assert k8s_app.input_topics == ["input-topic"]

        assert isinstance(k8s_apps[0], K8sAppDeployment)
        assert isinstance(k8s_apps[1], K8sAppStatefulSet)
        assert k8s_apps[1].get_service_name() == "test-service"

    def test_is_streams_bootstrap_app(self):
        streams_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic=None,
            )
        )
        assert streams_app.is_streams_bootstrap_app()

        non_streams_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics=None,
                output_topic=None,
                error_topic=None,
            )
        )
        assert not non_streams_app.is_streams_bootstrap_app()

    def test_error_topic_undefined(self):
        k8s_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic=None,
            )
        )
        assert k8s_app.name == "test-app"
        assert k8s_app.error_topic is None
        assert k8s_app.output_topic == "output-topic"
        assert k8s_app.input_topics == ["input-topic"]

    def test_multiple_inputs(self):
        k8s_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic1,input-topics2",
                output_topic="output-topic",
                error_topic="error-topic",
            )
        )
        assert k8s_app.input_topics == ["input-topic1", "input-topics2"]

    def test_env_prefix_support(self):
        k8s_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic="error-topic",
                env_prefix="TEST_",
            )
        )
        assert k8s_app.name == "test-app"
        assert k8s_app.error_topic == "error-topic"
        assert k8s_app.output_topic == "output-topic"
        assert k8s_app.input_topics == ["input-topic"]

    def test_extra_input_topics(self):
        k8s_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic="error-topic",
                multiple_inputs="0=test1,1=test2",
                env_prefix="TEST_",
            )
        )
        assert k8s_app.extra_input_topics == ["test1", "test2"]

    def test_extra_output_topics(self):
        k8s_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic="error-topic",
                multiple_outputs="0=test1,1=test2",
                env_prefix="TEST_",
            )
        )
        assert k8s_app.extra_output_topics == ["test1", "test2"]

    def test_attributes(self):
        k8s_app = K8sAppDeployment(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic="error-topic",
                multiple_outputs="0=test1,1=test2",
                env_prefix="TEST_",
                pipeline="pipeline1",
            )
        )
        assert k8s_app.attributes["pipeline"] == "pipeline1"
        assert len(k8s_app.attributes) == 1
