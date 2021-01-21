from streams_explorer.core.k8s_app import K8sApp
from tests.utils import get_streaming_app_deployment


class TestK8sApp:
    def test_init(self):
        k8s_app = K8sApp(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic",
                output_topic="output-topic",
                error_topic="error-topic",
            )
        )
        assert k8s_app.name == "test-app"
        assert k8s_app.error_topic == "error-topic"
        assert k8s_app.output_topic == "output-topic"
        assert k8s_app.input_topics == ["input-topic"]

    def test_error_topic_undefined(self):
        k8s_app = K8sApp(
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
        k8s_app = K8sApp(
            get_streaming_app_deployment(
                name="test-app",
                input_topics="input-topic1,input-topics2",
                output_topic="output-topic",
                error_topic="error-topic",
            )
        )
        assert k8s_app.input_topics == ["input-topic1", "input-topics2"]

    def test_env_prefix_support(self):
        k8s_app = K8sApp(
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
        k8s_app = K8sApp(
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
        k8s_app = K8sApp(
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
        k8s_app = K8sApp(
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
