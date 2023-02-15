from streams_explorer.core.extractor.extractor import ConnectorExtractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class RedisSinkConnector(KafkaConnector):
    pass


class RedisSink(ConnectorExtractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        config = info["config"]
        if (
            config.get("connector.class")
            == "com.github.jcustenborder.kafka.connect.redis.RedisSinkConnector"
        ):
            if topic := config.get("topics"):
                database = f"{topic}-db-{config['redis.database']}"
                self.sinks.append(
                    Sink(
                        node_type="database",
                        name=database,
                        source=connector_name,
                    )
                )
            topics = KafkaConnector.split_topics(config.get("topics"))
            return RedisSinkConnector(
                type=KafkaConnectorTypesEnum.SINK,
                name=connector_name,
                config=config,
                topics=topics,
                error_topic=None,
            )
