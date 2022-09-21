from streams_explorer.core.extractor.extractor import ConnectorExtractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class JdbcSink(ConnectorExtractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        config = info["config"]
        connector_class = config.get("connector.class")
        if connector_class and "JdbcSinkConnector" in connector_class:
            if name := config.get("table.name.format"):
                self.sinks.append(
                    Sink(
                        name=name,
                        node_type="jdbc-sink",
                        source=connector_name,
                    )
                )
            return KafkaConnector(
                name=connector_name,
                config=config,
                type=KafkaConnectorTypesEnum.SINK,
            )
