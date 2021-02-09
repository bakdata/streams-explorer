from typing import List

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class JdbcSink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(self, config, connector_name):
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
