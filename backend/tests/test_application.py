import asyncio

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from kubernetes.client import V1beta1CronJob, V1ObjectMeta

from streams_explorer.application import get_application
from streams_explorer.core.config import API_PREFIX, settings
from streams_explorer.streams_explorer import StreamsExplorer
from tests.utils import get_streaming_app_deployment


class TestApplication:
    @pytest.fixture()
    def client(self) -> TestClient:
        return TestClient(get_application())

    def test_redirect_from_root(self, client: TestClient):
        response = client.get("/", allow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/"

    def test_redirect_from_static(self, client: TestClient):
        response = client.get("/static", allow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/"

    def test_static_resources(self, client: TestClient):
        response = client.get("/static/.gitkeep")
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert response.content.decode() == ""

    @pytest.mark.asyncio
    async def test_update_every_x_seconds(self, mocker, monkeypatch):
        # workaround for exception "This event loop is already running"
        import nest_asyncio

        nest_asyncio.apply()
        settings.graph_update_every = 2

        def mock_get_deployments(*args, **kwargs):
            return [
                get_streaming_app_deployment(
                    "streaming-app1", "input-topic1", "output-topic1", "error-topic1"
                ),
                get_streaming_app_deployment(
                    "streaming-app2", "input-topic2", "output-topic2", "error-topic2"
                ),
                get_streaming_app_deployment(
                    "streaming-app3",
                    "input-topic3",
                    "output-topic3",
                    "error-topic3",
                    pipeline="pipeline2",
                ),
            ]

        def mock_get_cron_jobs(*args, **kwargs):
            return [V1beta1CronJob(metadata=V1ObjectMeta(name="test"))]

        monkeypatch.setattr(StreamsExplorer, "get_deployments", mock_get_deployments)
        monkeypatch.setattr(StreamsExplorer, "get_cron_jobs", mock_get_cron_jobs)
        monkeypatch.setattr(StreamsExplorer, "setup", lambda _: None)

        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
            lambda: ["connector1", "connector2"],
        )

        def get_connector_info(connector_name: str):
            if connector_name == "connector1":
                return {
                    "config": {
                        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
                        "topics": "output-topic1,output-topic2",
                        "test": "test_value",
                    },
                    "type": "sink",
                }
            return {
                "config": {
                    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
                    "topics": "output-topic3",
                    "transforms.changeTopic.replacement": "test-index",
                },
                "type": "sink",
            }

        mocker.patch(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connector_info",
            get_connector_info,
        )
        mocker.patch(
            "streams_explorer.extractors.load_extractors",
            lambda: None,
        )

        from main import app

        with TestClient(app) as client:
            await asyncio.sleep(0.1)
            response = client.get(f"{API_PREFIX}/graph")

            assert len(response.json().get("nodes")) == 15

            def mock_get_deployments(*args, **kwargs):
                return [
                    get_streaming_app_deployment(
                        "streaming-app1",
                        "input-topic1",
                        "output-topic1",
                        "error-topic1",
                    ),
                    get_streaming_app_deployment(
                        "streaming-app2",
                        "input-topic2",
                        "output-topic2",
                        "error-topic2",
                    ),
                ]

            monkeypatch.setattr(
                StreamsExplorer, "get_deployments", mock_get_deployments
            )
            await asyncio.sleep(2)
            response = client.get(f"{API_PREFIX}/graph")

            assert len(response.json().get("nodes")) == 12

            mocker.patch(
                "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
                lambda: ["connector1"],
            )
            await asyncio.sleep(2)
            response = client.get(f"{API_PREFIX}/graph")
            assert len(response.json().get("nodes")) == 9
