from streams_explorer.core.services import schemaregistry
from streams_explorer.core.services.schemaregistry import SchemaRegistry


def test_support_without_schemaregistry():
    schemaregistry.url = None
    assert SchemaRegistry.get_newest_topic_value_schema("test") == {}
