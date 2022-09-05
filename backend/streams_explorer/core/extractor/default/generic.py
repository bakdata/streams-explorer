from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)


class GenericSink(Extractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        if info["type"] == KafkaConnectorTypesEnum.SINK:
            config = info["config"]
            return KafkaConnector(
                name=connector_name,
                config=config,
                type=KafkaConnectorTypesEnum.SINK,
            )

    def reset_connector(self) -> None:
        self.reset()


class GenericSourceConnector(KafkaConnector):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            type=KafkaConnectorTypesEnum.SOURCE,
        )

    def get_topics(self) -> list[str]:
        return []


class GenericSource(Extractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        if info["type"] == KafkaConnectorTypesEnum.SOURCE:
            return GenericSourceConnector(name=connector_name, config=info["config"])

    def reset_connector(self) -> None:
        self.reset()
