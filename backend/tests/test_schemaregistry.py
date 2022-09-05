import pytest
import respx
from httpx import Response

from streams_explorer.core.services import schemaregistry
from streams_explorer.core.services.dataflow_graph import NodeNotFound
from streams_explorer.core.services.schemaregistry import SchemaRegistry

schemaregistry.url = "http://localhost:8081"
topic = "test-topic"


@respx.mock(base_url=schemaregistry.url)
def test_schemaregistry_versions(respx_mock: respx.MockRouter):
    mock_route = respx_mock.get(
        f"/subjects/{topic}-value/versions/",
    ).mock(return_value=Response(404))
    assert SchemaRegistry.get_versions(topic) == []

    versions = [1, 2, 3]
    mock_route.mock(return_value=Response(200, json=versions))
    assert SchemaRegistry.get_versions(topic) == versions


@respx.mock(base_url=schemaregistry.url)
def test_schemaregistry_schema(respx_mock: respx.MockRouter):
    version = 1
    respx_mock.get(f"/subjects/{topic}-value/versions/{version}").mock(
        return_value=Response(
            200,
            json={
                "subject": f"{topic}-value",
                "version": version,
                "id": version,
                "schema": '{"type":"record","name":"Test","namespace":"com.test","fields":[{"name":"first","type":"string"}]}',
            },
        )
    )
    assert SchemaRegistry.get_schema(topic, version=version) == {
        "type": "record",
        "name": "Test",
        "namespace": "com.test",
        "fields": [
            {"name": "first", "type": "string"},
        ],
    }


def test_schemaregistry_exception():
    with pytest.raises(NodeNotFound):
        SchemaRegistry.get_schema(topic)


def test_support_without_schemaregistry():
    schemaregistry.url = None
    assert SchemaRegistry.get_versions(topic) == []
    assert SchemaRegistry.get_schema(topic) == {}
