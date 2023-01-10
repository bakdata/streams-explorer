from streams_explorer.core.config import settings
from streams_explorer.core.extractor.default.elasticsearch_sink import ElasticsearchSink
from streams_explorer.core.extractor.default.jdbc_sink import JdbcSink
from streams_explorer.core.extractor.default.s3_sink import S3Sink
from streams_explorer.core.extractor.default.streams_bootstrap_producer import (
    StreamsBootstrapProducer,
)
from streams_explorer.core.extractor.extractor import Extractor
from streams_explorer.core.extractor.extractor_container import ExtractorContainer
from streams_explorer.plugins import load_plugin

extractor_container = ExtractorContainer()


def load_default() -> None:
    extractor_container.add(StreamsBootstrapProducer())
    extractor_container.add(ElasticsearchSink())
    extractor_container.add(S3Sink())
    extractor_container.add(JdbcSink())


if settings.plugins.extractors.default:
    load_default()


def load_extractors() -> None:
    extractors = load_plugin(Extractor, all=True)
    for extractor in extractors:
        extractor_container.add(extractor())
    extractor_container.add_generic()
