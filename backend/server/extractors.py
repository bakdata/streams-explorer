from server.core.config import settings
from server.core.extractor.default.elasticsearch_sink import ElasticsearchSink
from server.core.extractor.extractor import Extractor
from server.core.extractor.extractor_container import ExtractorContainer
from server.plugins import load_plugin

extractor_container = ExtractorContainer()

# add defaults
if settings.plugins.extractors.default:
    extractor_container.add(ElasticsearchSink())


def load_extractors():
    extractors = load_plugin(Extractor, all=True)
    for extractor in extractors:
        extractor_container.add(extractor())
