from typing import List

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class ElasticsearchSink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(self, config, connector_name):
        index = config.get("transforms.changeTopic.replacement")
        if index:
            self.sinks.append(
                Sink(
                    name=index,
                    node_type="elasticsearch-index",
                    source=connector_name,
                )
            )
