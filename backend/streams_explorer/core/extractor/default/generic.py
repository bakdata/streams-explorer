from typing import Optional

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)


class GenericSink(Extractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        if info["type"] == KafkaConnectorTypesEnum.SINK:
            config = info["config"]
            return KafkaConnector(
                name=connector_name,
                config=config,
                type=KafkaConnectorTypesEnum.SINK,
                topics=Extractor.split_topics(config.get("topics")),
                error_topic=config.get("errors.deadletterqueue.topic.name"),
            )
        return None


class GenericSource(Extractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        if info["type"] == KafkaConnectorTypesEnum.SOURCE:
            return KafkaConnector(
                name=connector_name,
                config=info["config"],
                type=KafkaConnectorTypesEnum.SOURCE,
                topics=[],
            )
        return None
