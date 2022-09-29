from streams_explorer.core.extractor.extractor import ConnectorExtractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class S3Sink(ConnectorExtractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        config = info["config"]
        connector_class = config.get("connector.class")
        if connector_class and "S3SinkConnector" in connector_class:
            if name := config.get("s3.bucket.name"):
                self.sinks.append(
                    Sink(
                        name=name,
                        node_type="s3-bucket",
                        source=connector_name,
                    )
                )
            return KafkaConnector(
                name=connector_name,
                config=config,
                type=KafkaConnectorTypesEnum.SINK,
            )
