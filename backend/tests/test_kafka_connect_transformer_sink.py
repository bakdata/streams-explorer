from typing import Literal

from pydantic import Field

from streams_explorer.core.extractor.default.transformer import RouterTransformerConfig
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorConfig,
    KafkaConnectorTypesEnum,
)


class TestTransformerKafkaConnect:
    def test_regex_router_transformer(self):
        connector = KafkaConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "transforms": "changeTopic",
                    "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.RegexRouter",
                    "transforms.changeTopic.regex": "my-(.*)",
                    "transforms.changeTopic.replacement": "index-$1",
                }
            ),
            topics=["my-topic-1", "my-topic-2"],
        )

        routes = connector.get_routes()
        assert len(routes) == 2
        assert "index-topic-1" in routes
        assert "index-topic-2" in routes

        connector = KafkaConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "transforms": "RemoveString",
                    "transforms.RemoveString.type": "org.apache.kafka.connect.transforms.RegexRouter",
                    "transforms.RemoveString.regex": "(.)Stream_(.)",
                    "transforms.RemoveString.replacement": "$1$2",
                }
            ),
            topics=["Order_Stream_Data"],
        )

        routes = connector.get_routes()
        assert len(routes) == 1
        assert "Order_Data" in routes, "Multiple regex groups should be substituted"

    def test_timestamp_router_transformer(self):
        connector = KafkaConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "transforms": "changeTopic",
                    "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.TimestampRouter",
                    "transforms.changeTopic.topic.format": "${topic}-${timestamp}",
                    "transforms.changeTopic.timestamp.format": "yyyyMMdd",
                }
            ),
            topics=["my-topic-1", "my-topic-2"],
        )
        routes = connector.get_routes()
        assert len(routes) == 2
        assert "my-topic-1-${yyyyMMdd}" in routes
        assert "my-topic-2-${yyyyMMdd}" in routes

    def test_regex_and_timestamp_router(self):
        connector = KafkaConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "transforms": "regexRouter,timestampRouter",
                    "transforms.regexRouter.type": "org.apache.kafka.connect.transforms.RegexRouter",
                    "transforms.regexRouter.regex": "my-(.*)",
                    "transforms.regexRouter.replacement": "index-$1",
                    "transforms.timestampRouter.type": "org.apache.kafka.connect.transforms.TimestampRouter",
                    "transforms.timestampRouter.topic.format": "${topic}-${timestamp}",
                    "transforms.timestampRouter.timestamp.format": "yyyyMMdd",
                }
            ),
            topics=["my-topic-1", "my-topic-2"],
        )

        routes = connector.get_routes()

        assert len(routes) == 2
        assert "index-topic-1-${yyyyMMdd}" in routes
        assert "index-topic-2-${yyyyMMdd}" in routes

    def test_unknown_transformer(self):
        connector = KafkaConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "transforms": "fakeTransformer",
                    "transforms.fakeTransformer.type": "org.apache.kafka.connect.transforms.FakeTransformer",
                }
            ),
            topics=["my-topic-1", "my-topic-2"],
        )

        routes = connector.get_routes()

        assert len(routes) == 2
        assert "my-topic-1" in routes
        assert "my-topic-2" in routes

        connector = KafkaConnector(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "transforms": "fakeTransformer,timestampRouter",
                    "transforms.fakeTransformer.type": "org.apache.kafka.connect.transforms.FakeTransformer",
                    "transforms.timestampRouter.type": "org.apache.kafka.connect.transforms.TimestampRouter",
                    "transforms.timestampRouter.topic.format": "${topic}-${timestamp}",
                    "transforms.timestampRouter.timestamp.format": "yyyyMMdd",
                }
            ),
            topics=["my-topic-1", "my-topic-2"],
        )

        routes = connector.get_routes()

        assert len(routes) == 2
        assert "my-topic-1-${yyyyMMdd}" in routes
        assert "my-topic-2-${yyyyMMdd}" in routes

    def test_custom_transformer(self):
        class CustomRouterTransformer(RouterTransformerConfig):
            _type: Literal["org.fake.kafka.CustomRouterTransformer"] = Field(
                ..., alias="type"
            )

            def transform_topic(self, topic: str) -> str:
                return "example-topic"

        class CustomKafkaConnectorTransformer(KafkaConnector):
            _transformers = CustomRouterTransformer

        connector = CustomKafkaConnectorTransformer(
            name="example-connector",
            type=KafkaConnectorTypesEnum.SINK,
            config=KafkaConnectorConfig(
                **{
                    "transforms": "changeTopic",
                    "transforms.changeTopic.type": "org.fake.kafka.CustomRouterTransformer",
                }
            ),
            topics=["my-topic-1", "my-topic-2"],
        )
        routes = connector.get_routes()
        assert len(routes) == 1
        assert "example-topic" in routes
