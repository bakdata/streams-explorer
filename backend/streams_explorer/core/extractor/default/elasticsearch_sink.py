from typing import List

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class ElasticsearchSink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(
        self, config: dict, connector_name: str
    ) -> List[str]:
        connector_class = config.get("connector.class")
        if connector_class and "ElasticsearchSinkConnector" in connector_class:
            index = config.get("transforms.changeTopic.replacement")
            if index:
                self.sinks.append(
                    Sink(
                        name=index,
                        node_type="elasticsearch-index",
                        source=connector_name,
                    )
                )
            return Extractor.split_topics(config.get("topics"))
        return []
