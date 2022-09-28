from streams_explorer.core.extractor.extractor import ConnectorExtractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class ElasticsearchSink(ConnectorExtractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        config = info["config"]
        connector_class: str | None = config.get("connector.class")
        if connector_class and "ElasticsearchSinkConnector" in connector_class:

            connector = KafkaConnector(
                name=connector_name,
                config=config,
                type=KafkaConnectorTypesEnum.SINK,
            )
            indices = connector.get_routes()
            for index in indices:
                self.sinks.append(
                    Sink(
                        name=index,
                        node_type="elasticsearch-index",
                        source=connector_name,
                    )
                )
            return connector
