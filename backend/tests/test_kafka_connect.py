import respx
from httpx import Response

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
    kafkaconnect.url = "http://localhost:8083"

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

    @respx.mock(base_url=kafkaconnect.url)
    def test_sanitize_connector_config(self, respx_mock: respx.MockRouter):
        connector_config = {
            "connector.class": "ConnectorClass",
            "connection.password": "supersecret",
        }
        mock_route = respx_mock.put(
            f"/connector-plugins/{connector_config['connector.class']}/config/validate",
        ).mock(return_value=Response(200, json=connector_data))
        for _ in range(2):
            assert KafkaConnect.sanitize_connector_config(connector_config) == {
                "connector.class": "ConnectorClass",
                "connection.password": "[hidden]",
            }
        assert mock_route.call_count == 1  # Verify caching works
