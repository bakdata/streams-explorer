from dataclasses import dataclass
from typing import Dict, List, Optional

import pytest
from confluent_kafka.admin import ConfigEntry, ConfigResource, PartitionMetadata

from streams_explorer.core.services.kafka import Kafka

test_topic = "test-topic"


class TestKafka:
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

        def mock_get_resource(resource: ConfigResource, *args) -> List[ConfigEntry]:
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
