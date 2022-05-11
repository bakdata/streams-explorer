import asyncio
from typing import List

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from kubernetes_asyncio.client import (
    V1beta1CronJob,
    V1Deployment,
    V1ObjectMeta,
    V1StatefulSet,
)

from streams_explorer.application import get_application
from streams_explorer.core.config import API_PREFIX, settings
from streams_explorer.streams_explorer import StreamsExplorer
from tests.utils import get_streaming_app_deployment


class TestApplication:
    @pytest.fixture(autouse=True)
    def kafka_connect(self):
        settings.kafkaconnect.url = "testurl:3000"

    @pytest.fixture()
    def client(self) -> TestClient:
        return TestClient(get_application())

    def test_static_resources(self, client: TestClient):
        response = client.get("/.gitkeep")
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert response.content.decode() == ""

    @pytest.fixture()
    def deployments(self) -> List[V1Deployment]:
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

    # def deployments_after(self):
    #     return [
    #         get_streaming_app_deployment(
    #             "streaming-app1",
    #             "input-topic1",
    #             "output-topic1",
    #             "error-topic1",
    #         ),
    #         get_streaming_app_deployment(
    #             "streaming-app2",
    #             "input-topic2",
    #             "output-topic2",
    #             "error-topic2",
    #         ),
    #     ]

    @pytest.fixture()
    def stateful_sets(self) -> List[V1StatefulSet]:
        return []

    @pytest.fixture()
    def cron_jobs(self) -> List[V1beta1CronJob]:
        return [V1beta1CronJob(metadata=V1ObjectMeta(name="test"))]

    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_update_every_x_seconds(
        self, mocker, monkeypatch, deployments, stateful_sets, cron_jobs
    ):
        # workaround for exception "This event loop is already running"
        import nest_asyncio

        nest_asyncio.apply()
        settings.graph.update_interval = 2

        async def watch(self):
            for deployment in deployments + cron_jobs:
                event = {"type": "ADDED", "object": deployment}
                self.handle_event(event)

        monkeypatch.setattr(StreamsExplorer, "setup", self.setup)
        monkeypatch.setattr(StreamsExplorer, "watch", watch)

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
                    "transforms": "changeTopic",
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

    @pytest.mark.asyncio
    async def test_pipeline_not_found(self, monkeypatch):
        from main import app

        async def setup(_):
            pass

        monkeypatch.setattr(StreamsExplorer, "setup", setup)

        with TestClient(app) as client:
            response = client.get(
                f"{API_PREFIX}/graph", params={"pipeline_name": "doesnt-exist"}
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Pipeline 'doesnt-exist' not found"
