from typing import List, Optional

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class JdbcSink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        config = info["config"]
        connector_class = config.get("connector.class")
        if connector_class and "JdbcSinkConnector" in connector_class:
            name = config.get("table.name.format")
            if name:
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
                topics=Extractor.split_topics(config.get("topics")),
                error_topic=config.get("errors.deadletterqueue.topic.name"),
            )
        return None
