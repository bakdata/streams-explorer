from streams_explorer.core.config import settings
from streams_explorer.core.services import kafkaconnect
from streams_explorer.core.services.kafkaconnect import KafkaConnect

connector_data = {
    "configs": [
        {
            "definition": {
                "name": "connection.password",
                "type": "PASSWORD",
                "display_name": "Connection Password",
            },
            "value": {
                "name": "connection.password",
                "value": "[hidden]",
            },
        },
    ]
}


class TestKafkaConnect:
    def test_extract_connector_class_basename(self):
        assert (
            KafkaConnect.extract_connector_class_basename(
                "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector"
            )
            == "ElasticsearchSinkConnector"
        )
        assert (
            KafkaConnect.extract_connector_class_basename("ElasticsearchSinkConnector")
            == "ElasticsearchSinkConnector"
        )

    def test_sanitize_connector_config(self, requests_mock):
        kafkaconnect.url = "http://testurl:3000"
        connector_config = {
            "connector.class": "ConnectorClass",
            "connection.password": "supersecret",
        }
        requests_mock.put(
            f"{kafkaconnect.url}/connector-plugins/{connector_config['connector.class']}/config/validate",
            json=connector_data,
        )
        for _ in range(2):
            assert KafkaConnect.sanitize_connector_config(connector_config) == {
                "connector.class": "ConnectorClass",
                "connection.password": "[hidden]",
            }
        assert requests_mock.call_count == 1  # Verify caching works

    def test_without_kafka_connect(self):
        settings.kafkaconnect.url = None
        assert KafkaConnect.connectors() == []
