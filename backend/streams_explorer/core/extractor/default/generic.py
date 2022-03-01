from typing import List, Optional

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
            )
        return None


class GenericSourceConnector(KafkaConnector):
    def get_topics(self) -> List[str]:
        return []


class GenericSource(Extractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        if info["type"] == KafkaConnectorTypesEnum.SOURCE:
            return GenericSourceConnector(
                name=connector_name,
                config=info["config"],
                type=KafkaConnectorTypesEnum.SOURCE,
            )
        return None
