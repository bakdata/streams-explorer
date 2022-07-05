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
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from streams_explorer.application import get_application
from streams_explorer.core.client_manager import ClientManager
from streams_explorer.core.config import API_PREFIX, settings
from streams_explorer.core.services.kafkaconnect import KafkaConnect
from streams_explorer.core.services.kubernetes import K8sDeploymentUpdate
from streams_explorer.models.k8s import K8sDeploymentUpdateType
from streams_explorer.streams_explorer import StreamsExplorer
from tests.utils import get_streaming_app_deployment


async def mock_setup(_):
    pass


APP1 = get_streaming_app_deployment(
    "streaming-app1", "input-topic1", "output-topic1", "error-topic1"
)
APP2 = get_streaming_app_deployment(
    "streaming-app2", "input-topic2", "output-topic2", "error-topic2"
)
APP3 = get_streaming_app_deployment(
    "streaming-app3",
    "input-topic3",
    "output-topic3",
    "error-topic3",
    pipeline="pipeline2",
)


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
        return [APP1, APP2, APP3]

    @pytest.fixture()
    def stateful_sets(self) -> List[V1StatefulSet]:
        return []

    @pytest.fixture()
    def cron_jobs(self) -> List[V1beta1CronJob]:
        return [V1beta1CronJob(metadata=V1ObjectMeta(name="test"))]

    @pytest.mark.asyncio
    async def test_update_every_x_seconds(
        self, mocker, monkeypatch, deployments, stateful_sets, cron_jobs
    ):
        settings.graph.update_interval = 1
        settings.kafkaconnect.update_interval = 1

        async def watch(self):
            for deployment in deployments + stateful_sets + cron_jobs:
                event = K8sDeploymentUpdate(
                    type=K8sDeploymentUpdateType.ADDED, object=deployment
                )
                await self.handle_deployment_update(event)

        monkeypatch.setattr(StreamsExplorer, "setup", mock_setup)
        monkeypatch.setattr(StreamsExplorer, "watch", watch)

        connectors = ["connector1", "connector2"]
        monkeypatch.setattr(
            "streams_explorer.core.services.kafkaconnect.KafkaConnect.get_connectors",
            lambda: connectors,
        )
        assert KafkaConnect.get_connectors() == connectors

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

            def fetch_graph() -> List[str]:
                response = client.get(f"{API_PREFIX}/graph")
                return [node["id"] for node in response.json()["nodes"]]

            await asyncio.sleep(1)

            nodes = fetch_graph()
            assert "streaming-app1" in nodes
            assert "streaming-app2" in nodes
            assert "streaming-app3" in nodes
            assert "connector1" in nodes
            assert "connector2" in nodes
            assert "input-topic1" in nodes
            assert "output-topic1" in nodes
            assert "error-topic1" in nodes
            assert "input-topic2" in nodes
            assert "output-topic2" in nodes
            assert "error-topic2" in nodes
            assert "input-topic3" in nodes
            assert "output-topic3" in nodes
            assert "error-topic3" in nodes
            assert "test-index" in nodes
            assert len(nodes) == 15

            # destroy a deployment
            update = K8sDeploymentUpdate(
                type=K8sDeploymentUpdateType.DELETED, object=APP3
            )
            await app.state.streams_explorer.handle_deployment_update(update)

            await asyncio.sleep(1)  # update graph
            nodes = fetch_graph()
            assert "streaming-app1" in nodes
            assert "streaming-app2" in nodes
            assert "streaming-app3" not in nodes
            assert "connector1" in nodes
            assert "connector2" in nodes
            assert "input-topic1" in nodes
            assert "output-topic1" in nodes
            assert "error-topic1" in nodes
            assert "input-topic2" in nodes
            assert "output-topic2" in nodes
            assert "error-topic2" in nodes
            assert "input-topic3" not in nodes
            assert "output-topic3" in nodes
            assert "error-topic3" not in nodes
            assert "test-index" in nodes
            assert len(nodes) == 12

            # remove a connector
            connectors = ["connector1"]
            assert KafkaConnect.get_connectors() == connectors

            await asyncio.sleep(2)  # update connectors
            assert len(app.state.streams_explorer.kafka_connectors) == 1
            assert app.state.streams_explorer.kafka_connectors[0].name == "connector1"

            await asyncio.sleep(1)  # update graph
            nodes = fetch_graph()
            assert "streaming-app1" in nodes
            assert "streaming-app2" in nodes
            assert "streaming-app3" not in nodes
            assert "connector1" in nodes
            assert "connector2" not in nodes
            assert "input-topic1" in nodes
            assert "output-topic1" in nodes
            assert "error-topic1" in nodes
            assert "input-topic2" in nodes
            assert "output-topic2" in nodes
            assert "error-topic2" in nodes
            assert "input-topic3" not in nodes
            assert "test-index" not in nodes
            assert len(nodes) == 9

    @pytest.mark.asyncio
    async def test_pipeline_not_found(self, monkeypatch):
        from main import app

        monkeypatch.setattr(StreamsExplorer, "setup", mock_setup)

        with TestClient(app) as client:
            response = client.get(
                f"{API_PREFIX}/graph", params={"pipeline_name": "doesnt-exist"}
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Pipeline 'doesnt-exist' not found"

    def test_websocket(
        self,
        monkeypatch: MonkeyPatch,
        mocker: MockerFixture,
        deployments,
        stateful_sets,
        cron_jobs,
    ):
        settings.graph.update_interval = 1
        settings.kafkaconnect.update_interval = 1

        async def watch(self: StreamsExplorer):
            for deployment in deployments + stateful_sets + cron_jobs:
                event = K8sDeploymentUpdate(
                    type=K8sDeploymentUpdateType.ADDED, object=deployment
                )
                await self.handle_deployment_update(event)
            # object = {
            #     "type": K8sEventType.NORMAL,
            #     "reason": "Starting",
            #     "regarding": {
            #         "fieldPath": "spec.containers{atm-fraud-transactionavroproducer}",
            #         "namespace": "test-namespace",
            #     },
            # }
            # event = K8sEvent(type=K8sEventType.NORMAL, object=object)
            # await self.handle_event(event)

        monkeypatch.setattr(StreamsExplorer, "setup", mock_setup)
        monkeypatch.setattr(StreamsExplorer, "watch", watch)

        from main import app

        update_client_full = mocker.spy(StreamsExplorer, "update_client_full")
        connect = mocker.spy(ClientManager, "connect")
        with TestClient(app) as client:
            with client.websocket_connect("/api/graph/ws") as websocket:
                connect.assert_called_once()
                data = websocket.receive_json()
                update_client_full.assert_called_once()
                assert data == {
                    "id": "streaming-app1",
                    "replicas": [None, None],
                    "state": "Unknown",
                }
                data = websocket.receive_json()
                assert data == {
                    "id": "streaming-app2",
                    "replicas": [None, None],
                    "state": "Unknown",
                }
                data = websocket.receive_json()
                assert data == {
                    "id": "streaming-app3",
                    "replicas": [None, None],
                    "state": "Unknown",
                }
                websocket.close()
