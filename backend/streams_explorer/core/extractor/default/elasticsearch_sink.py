from typing import List, Optional

import pydantic
from loguru import logger
from pydantic import ValidationError

from streams_explorer.core.extractor.default.transformer import TRANSFORMER
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.kafka_connector import (
    KafkaConnector,
    KafkaConnectorTypesEnum,
)
from streams_explorer.models.sink import Sink


class ElasticSearchSinkConnector(KafkaConnector):
    def get_topics(self) -> List[str]:
        return Extractor.split_topics(self.config.topics)

    def get_indices(self) -> List[str]:
        indices = self.get_topics()
        transforms = self.config.get_transforms()
        for transformer_name in transforms:
            indices = self.apply_transformer(indices, transformer_name)
        return list(set(indices))

    def apply_transformer(self, indices, transformer_name) -> List[str]:
        transformer_prefix = ElasticSearchSinkConnector.get_transformer_prefix(
            transformer_name
        )
        # transformer config without transformer_prefix
        transformer_config = {
            config_name.replace(transformer_prefix, ""): config_value
            for config_name, config_value in self.config.dict().items()
            if ElasticSearchSinkConnector.is_transformer_config(
                config_name, transformer_prefix
            )
        }
        transformer_config["topics"] = indices
        try:
            transformer = pydantic.parse_obj_as(TRANSFORMER, transformer_config)
            return transformer.get_routes()
        except ValidationError as e:
            logger.exception(
                f"Failed to apply transformer {transformer_name} on {self.name}", e
            )
            return []

    @staticmethod
    def get_transformer_prefix(transformer_name: str) -> str:
        return f"transforms.{transformer_name}."

    @staticmethod
    def is_transformer_config(key: str, transformer_prefix: str) -> bool:
        return key.startswith(transformer_prefix)


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
            indices = connector.get_indices()
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
