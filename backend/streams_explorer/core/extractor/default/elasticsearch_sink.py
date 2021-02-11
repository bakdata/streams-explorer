from typing import List, Optional

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class ElasticsearchSink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []
        self.topics: List[str] = []

    def on_connector_config_parsing(self, config: dict, connector_name: str):
        connector_class = config.get("connector.class")
        if connector_class and "ElasticsearchSinkConnector" in connector_class:
            self.topics = self.split_topics(config.get("topics"))
            index = config.get("transforms.changeTopic.replacement")
            if index:
                self.sinks.append(
                    Sink(
                        name=index,
                        node_type="elasticsearch-index",
                        source=connector_name,
                    )
                )

    @staticmethod
    def split_topics(topics: Optional[str]) -> List[str]:
        if topics is not None:
            return topics.replace(" ", "").split(",")
        return []
