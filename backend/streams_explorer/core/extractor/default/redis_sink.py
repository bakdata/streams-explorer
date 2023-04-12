from streams_explorer.core.extractor.extractor import ConnectorExtractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class RedisSinkConnector(KafkaConnector):
    def __init__(self, **kwargs) -> None:
        super().__init__(type=KafkaConnectorTypesEnum.SINK, **kwargs)


class RedisSink(ConnectorExtractor):
    def on_connector_info_parsing(
        self, info: dict, connector_name: str
    ) -> KafkaConnector | None:
        config = info["config"]
        if (
            config.get("connector.class")
            == "com.github.jcustenborder.kafka.connect.redis.RedisSinkConnector"
        ):
            database = f"{config['redis.hosts']}-db-{config['redis.database']}"
            self.sinks.append(
                Sink(
                    node_type="database",
                    name=database,
                    source=connector_name,
                )
            )
            return RedisSinkConnector(name=connector_name, config=config)
