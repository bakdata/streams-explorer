from dataclasses import dataclass
from typing import Dict, List, Optional

import pytest
from confluent_kafka.admin import ConfigEntry, ConfigResource, PartitionMetadata
from dynaconf.validator import ValidationError

from streams_explorer.core.config import settings
from streams_explorer.core.services.kafka import Kafka

test_topic = "test-topic"


class TestKafka:
    def test_kafka_settings(self):
        settings.kafka.enable = True
        settings.validators.validate()

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
        assert Kafka.format_values(raw) == {"key": "value"}
        assert Kafka.format_values([]) == {}

    @pytest.fixture()
    def kafka(self, monkeypatch) -> Kafka:
        kafka = Kafka()

        def mock_get_resource(resource: ConfigResource, *_) -> List[ConfigEntry]:
            if resource == ConfigResource(ConfigResource.Type.TOPIC, test_topic):
                return [
                    ConfigEntry(name="cleanup.policy", value="delete"),
                    ConfigEntry(name="retention.ms", value="-1"),
                ]
            return []

        monkeypatch.setattr(kafka, "_Kafka__get_resource", mock_get_resource)

        @dataclass
        class MockTopicMetadata:
            topic: str
            partitions: Dict[int, PartitionMetadata]

        def mock_get_topic(topic: str) -> Optional[MockTopicMetadata]:
            if topic == test_topic:
                meta = PartitionMetadata()
                partitions = {i: meta for i in range(10)}
                return MockTopicMetadata(test_topic, partitions)
            return None

        monkeypatch.setattr(kafka, "_Kafka__get_topic", mock_get_topic)

        return kafka

    def test_get_topic_config(self, kafka: Kafka):
        assert kafka.get_topic_config(test_topic) == {
            "cleanup.policy": "delete",
            "retention.ms": "-1",
        }
        assert kafka.get_topic_config("doesnt-exist") == {}

    def test_get_topic_partitions(self, kafka: Kafka):
        partitions = kafka.get_topic_partitions(test_topic)
        assert type(partitions) is dict
        assert len(partitions) == 10
        assert kafka.get_topic_partitions("doesnt-exist") is None
