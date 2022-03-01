from streams_explorer.core.extractor.default.elasticsearch_sink import (
    ElasticSearchSinkConnector,
)
from streams_explorer.models.kafka_connector import (
    KafkaConnectorConfig,
    KafkaConnectorTypesEnum,
)


class TestElasticSearchSinkConnector:
    def test_regex_router_transformer(self):
        elastic_sink_connector = ElasticSearchSinkConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "topics": "my-topic-1,my-topic-2",
                    "transforms": "changeTopic",
                    "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.RegexRouter",
                    "transforms.changeTopic.regex": "my-(.*)",
                    "transforms.changeTopic.replacement": "index-$1",
                }
            ),
        )

        indices = elastic_sink_connector.get_routes()
        assert len(indices) == 2
        assert "index-topic-1" in indices
        assert "index-topic-2" in indices

        elastic_sink_connector = ElasticSearchSinkConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "topics": "Order_Stream_Data",
                    "transforms": "RemoveString",
                    "transforms.RemoveString.type": "org.apache.kafka.connect.transforms.RegexRouter",
                    "transforms.RemoveString.regex": "(.)Stream_(.)",
                    "transforms.RemoveString.replacement": "$1$2",
                }
            ),
        )

        indices = elastic_sink_connector.get_routes()
        assert len(indices) == 1
        assert "Order_Data" in indices, "Multiple regex groups should be substituted"

    def test_timestamp_router_transformer(self):
        elastic_sink_connector = ElasticSearchSinkConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "topics": "my-topic-1,my-topic-2",
                    "transforms": "changeTopic",
                    "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.TimestampRouter",
                    "transforms.changeTopic.topic.format": "${topic}-${timestamp}",
                    "transforms.changeTopic.timestamp.format": "yyyyMMdd",
                }
            ),
        )
        indices = elastic_sink_connector.get_routes()
        assert len(indices) == 2
        assert "my-topic-1-${yyyyMMdd}" in indices
        assert "my-topic-2-${yyyyMMdd}" in indices

    def test_regex_and_timestamp_router(self):
        elastic_sink_connector = ElasticSearchSinkConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "topics": "my-topic-1,my-topic-2",
                    "transforms": "regexRouter,timestampRouter",
                    "transforms.regexRouter.type": "org.apache.kafka.connect.transforms.RegexRouter",
                    "transforms.regexRouter.regex": "my-(.*)",
                    "transforms.regexRouter.replacement": "index-$1",
                    "transforms.timestampRouter.type": "org.apache.kafka.connect.transforms.TimestampRouter",
                    "transforms.timestampRouter.topic.format": "${topic}-${timestamp}",
                    "transforms.timestampRouter.timestamp.format": "yyyyMMdd",
                }
            ),
        )

        indices = elastic_sink_connector.get_routes()

        assert len(indices) == 2
        assert "index-topic-1-${yyyyMMdd}" in indices
        assert "index-topic-2-${yyyyMMdd}" in indices
