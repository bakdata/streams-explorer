from typing import List

import pytest
from confluent_kafka.admin import ConfigEntry, ConfigResource

from streams_explorer.core.services.kafka import Kafka


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
            if resource == ConfigResource(ConfigResource.Type.TOPIC, "test-topic"):
                return [ConfigEntry(name="cleanup.policy", value="delete")]
            return []

        monkeypatch.setattr(kafka, "_Kafka__get_resource", mock_get_resource)
        return kafka

    def test_get_topic_config(self, kafka):
        assert kafka.get_topic_config("test-topic") == {"cleanup.policy": "delete"}
        assert kafka.get_topic_config("doesnt-exist") == {}
