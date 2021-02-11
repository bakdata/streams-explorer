from typing import List

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.sink import Sink


class S3Sink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(
        self, config: dict, connector_name: str
    ) -> List[str]:
        connector_class = config.get("connector.class")
        if connector_class and "S3SinkConnector" in connector_class:
            name = config.get("s3.bucket.name")
            if name:
                self.sinks.append(
                    Sink(
                        name=name,
                        node_type="s3-bucket",
                        source=connector_name,
                    )
                )
            return Extractor.split_topics(config.get("topics"))
        return []
