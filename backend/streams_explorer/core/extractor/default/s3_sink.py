from typing import List

from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.models.node_types import NodeTypesEnum
from streams_explorer.models.sink import Sink


class S3Sink(Extractor):
    def __init__(self):
        self.sinks: List[Sink] = []

    def on_connector_config_parsing(self, config, connector_name):
        if "S3SinkConnector" in config.get("connector.class"):
            self.sinks.append(
                Sink(
                    name=config.get("s3.bucket.name"),
                    node_type=NodeTypesEnum.SINK_SOURCE,
                    # node_type="s3-bucket",
                    source=connector_name,
                )
            )
