from typing import List

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class JdbcSink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(self, config, connector_name):
        if "JdbcSinkConnector" in config.get("connector.class"):
            self.sinks.append(
                Sink(
                    name=config.get("name"),
                    node_type="jdbc-sink",
                    source=connector_name,
                )
            )
