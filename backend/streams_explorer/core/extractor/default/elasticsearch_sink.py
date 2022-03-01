from typing import List, Optional

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class ElasticSearchSinkConnector(KafkaConnector):
    def get_topics(self) -> List[str]:
        return Extractor.split_topics(self.config.topics)


class ElasticsearchSink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> Optional[KafkaConnector]:
        config = info["config"]
        connector_class = config.get("connector.class")
        if connector_class and "ElasticsearchSinkConnector" in connector_class:

            connector = ElasticSearchSinkConnector(
                name=connector_name,
                config=config,
                type=KafkaConnectorTypesEnum.SINK,
                error_topic=config.get("errors.deadletterqueue.topic.name"),
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
        return None
