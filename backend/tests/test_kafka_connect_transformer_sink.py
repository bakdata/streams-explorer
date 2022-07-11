from typing import Literal

import pytest
from pydantic import Field

from streams_explorer.core.extractor.default.transformer import RouterTransformerConfig
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorConfig,
    KafkaConnectorTypesEnum,
)


class TestTransformerKafkaConnect:
    @pytest.mark.parametrize(
        ("connector", "expected_routes", "fail_message"),
        [
            (
                KafkaConnector(
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
                ),
                {"index-topic-1", "index-topic-2"},
                None,
            ),
            (
                KafkaConnector(
                    name="example-connector",
                    type=KafkaConnectorTypesEnum.SINK,
                    config=KafkaConnectorConfig(
                        **{
                            "transforms": "changeTopic",
                            "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.RegexRouter",
                            "transforms.changeTopic.regex": ".*",
                            "transforms.changeTopic.replacement": "fake-index",
                        }
                    ),
                    topics=["my-topic-1", "my-topic-2"],
                ),
                {"fake-indexfake-index"},
                None,
            ),
            (
                KafkaConnector(
                    name="example-connector",
                    type=KafkaConnectorTypesEnum.SINK,
                    config=KafkaConnectorConfig(
                        **{
                            "transforms": "changeTopic",
                            "transforms.changeTopic.type": "org.apache.kafka.connect.transforms.RegexRouter",
                            "transforms.changeTopic.regex": "^.*",
                            "transforms.changeTopic.replacement": "fake-index",
                        }
                    ),
                    topics=["my-topic-1", "my-topic-2"],
                ),
                {"fake-index"},
                None,
            ),
            (
                KafkaConnector(
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
                ),
                {"Order_Data"},
                "Multiple regex groups should be substituted",
            ),
        ],
    )
    def test_regex_router_transformer(
        self,
        connector: KafkaConnector,
        expected_routes: set[str],
        fail_message: str | None,
    ):
        assert connector.get_routes() == expected_routes, fail_message

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
        assert connector.get_routes() == {
            "my-topic-1-${yyyyMMdd}",
            "my-topic-2-${yyyyMMdd}",
        }

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

        assert connector.get_routes() == {
            "index-topic-1-${yyyyMMdd}",
            "index-topic-2-${yyyyMMdd}",
        }

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

        assert connector.get_routes() == {"my-topic-1", "my-topic-2"}

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

        assert connector.get_routes() == {
            "my-topic-1-${yyyyMMdd}",
            "my-topic-2-${yyyyMMdd}",
        }

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
        assert connector.get_routes() == {"example-topic"}
