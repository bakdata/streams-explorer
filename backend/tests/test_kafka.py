from dataclasses import dataclass

import pytest
from confluent_kafka.admin import ConfigEntry, ConfigResource, PartitionMetadata
from dynaconf.validator import ValidationError
from pytest import MonkeyPatch

from streams_explorer.core.config import settings
from streams_explorer.core.services.kafka_admin_client import KafkaAdminClient

test_topic = "test-topic"


class TestKafka:
    def test_settings(self):
        # validate default
        settings.kafka.enable = True
        settings.validators.validate()

        # should fail if no broker is set
        settings.kafka.config = {"bootstrap.servers": None}
        with pytest.raises(ValidationError):
            settings.validators.validate()

        # should disable when no Kafka settings are given
        del settings.kafka.enable
        del settings.kafka.config
        settings.validators.validate()
        assert settings.kafka.enable is False

        # reset
        settings.kafka.config = {"bootstrap.servers": "localhost:9092"}

    def test_format_values(self):
        raw = [
            ConfigEntry(name="key", value="value"),
            ConfigEntry(name="sensitive", value="supersecret", is_sensitive=True),
        ]
        assert KafkaAdminClient.format_values(raw) == {"key": "value"}
        assert KafkaAdminClient.format_values([]) == {}

    @pytest.fixture()
    def kafka(self, monkeypatch: MonkeyPatch) -> KafkaAdminClient:
        kafka = KafkaAdminClient()

        def mock_get_resource(resource: ConfigResource, *_) -> list[ConfigEntry]:
            if resource == ConfigResource(ConfigResource.Type.TOPIC, test_topic):
                return [
                    ConfigEntry(name="cleanup.policy", value="delete"),
                    ConfigEntry(name="retention.ms", value="-1"),
                ]
            return []

        monkeypatch.setattr(kafka, "_KafkaAdminClient__get_resource", mock_get_resource)

        @dataclass
        class MockTopicMetadata:
            topic: str
            partitions: dict[int, PartitionMetadata]

        def mock_get_topic(topic: str) -> MockTopicMetadata | None:
            if topic == test_topic:
                meta = PartitionMetadata()
                partitions = {i: meta for i in range(10)}
                return MockTopicMetadata(test_topic, partitions)

        monkeypatch.setattr(kafka, "_KafkaAdminClient__get_topic", mock_get_topic)

        return kafka

    def test_get_topic_config(self, kafka: KafkaAdminClient):
        assert kafka.get_topic_config(test_topic) == {
            "cleanup.policy": "delete",
            "retention.ms": "-1",
        }
        assert kafka.get_topic_config("doesnt-exist") == {}

    def test_get_topic_partitions(self, kafka: KafkaAdminClient):
        partitions = kafka.get_topic_partitions(test_topic)
        assert type(partitions) is dict
        assert len(partitions) == 10
        assert kafka.get_topic_partitions("doesnt-exist") is None
