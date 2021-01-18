from enum import Enum


class NodeTypesEnum(str, Enum):
    STREAMING_APP = "streaming-app"
    CONNECTOR = "connector"
    TOPIC = "topic"
    ERROR_TOPIC = "error-topic"
    SINK_SOURCE = "sink/source"
