import asyncio
import datetime
from time import sleep

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from kubernetes_asyncio.client import (
    EventsV1Event,
    V1CronJob,
    V1Deployment,
    V1ObjectMeta,
    V1ObjectReference,
    V1StatefulSet,
)
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from streams_explorer.api.dependencies.streams_explorer import (
    get_streams_explorer_from_state,
)
from streams_explorer.application import get_application
from streams_explorer.core.client_manager import ClientManager
from streams_explorer.core.config import API_PREFIX, settings
from streams_explorer.core.k8s_app import K8sObject
from streams_explorer.core.services.kafkaconnect import KafkaConnect
from streams_explorer.core.services.kubernetes import K8sDeploymentUpdate, K8sEvent
from streams_explorer.models.k8s import K8sDeploymentUpdateType, K8sEventType, K8sReason
from streams_explorer.streams_explorer import StreamsExplorer
from tests.utils import get_streaming_app_deployment

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


WS_ENDPOINT = "/api/graph/ws"


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
    def deployments(self) -> list[V1Deployment]:
        return [APP1, APP2, APP3]

    @pytest.fixture()
    def stateful_sets(self) -> list[V1StatefulSet]:
        return []

    @pytest.fixture()
    def cron_jobs(self) -> list[V1CronJob]:
        return [V1CronJob(metadata=V1ObjectMeta(name="test"))]

    @pytest.mark.asyncio
    async def test_update_every_x_seconds(
        self,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        deployments: list[K8sObject],
        stateful_sets: list[K8sObject],
        cron_jobs: list[K8sObject],
    ):
        settings.graph.update_interval = 1
        settings.kafkaconnect.update_interval = 1

        async def watch(self: StreamsExplorer):
            for deployment in deployments + stateful_sets + cron_jobs:
                event = K8sDeploymentUpdate(
                    type=K8sDeploymentUpdateType.ADDED, object=deployment
                )
                await self.handle_deployment_update(event)

        mocker.patch.object(StreamsExplorer, "setup")
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
            streams_explorer = get_streams_explorer_from_state(app)

            def fetch_graph() -> list[str]:
                response = client.get(f"{API_PREFIX}/graph")
                return [node["id"] for node in response.json()["nodes"]]

            await asyncio.sleep(1)

            nodes = fetch_graph()
            assert "test-namespace/streaming-app1" in nodes
            assert "test-namespace/streaming-app2" in nodes
            assert "test-namespace/streaming-app3" in nodes
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
            await streams_explorer.handle_deployment_update(update)

            await asyncio.sleep(1)  # update graph
            nodes = fetch_graph()
            assert "test-namespace/streaming-app1" in nodes
            assert "test-namespace/streaming-app2" in nodes
            assert "test-namespace/streaming-app3" not in nodes
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
            assert len(streams_explorer.kafka_connectors) == 1
            assert streams_explorer.kafka_connectors[0].name == "connector1"

            await asyncio.sleep(1)  # update graph
            nodes = fetch_graph()
            assert "test-namespace/streaming-app1" in nodes
            assert "test-namespace/streaming-app2" in nodes
            assert "test-namespace/streaming-app3" not in nodes
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
    async def test_pipeline_not_found(self, mocker: MockerFixture):
        from main import app

        mocker.patch.object(StreamsExplorer, "setup")

        with TestClient(app) as client:
            response = client.get(
                f"{API_PREFIX}/graph", params={"pipeline_name": "doesnt-exist"}
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Pipeline 'doesnt-exist' not found"

    @pytest.mark.asyncio
    async def test_websocket(
        self,
        monkeypatch: MonkeyPatch,
        mocker: MockerFixture,
        deployments: list[K8sObject],
        stateful_sets: list[K8sObject],
        cron_jobs: list[K8sObject],
    ):
        async def watch(self: StreamsExplorer):
            for deployment in deployments + stateful_sets + cron_jobs:
                update = K8sDeploymentUpdate(
                    type=K8sDeploymentUpdateType.ADDED, object=deployment
                )
                await self.handle_deployment_update(update)
            object = EventsV1Event(
                type=K8sEventType.NORMAL,
                reason=K8sReason.STARTED,
                regarding=V1ObjectReference(
                    field_path="spec.containers{streaming-app2}",
                    namespace="test-namespace",
                ),
                event_time=datetime.datetime.now(),
            )
            event = K8sEvent(type=K8sEventType.NORMAL, object=object)
            await self.handle_event(event)
            object = EventsV1Event(
                type=K8sEventType.WARNING,
                reason=K8sReason.BACKOFF,
                regarding=V1ObjectReference(
                    field_path="spec.containers{streaming-app3}",
                    namespace="test-namespace",
                ),
                event_time=datetime.datetime.now(),
            )
            event = K8sEvent(type=K8sEventType.WARNING, object=object)
            await self.handle_event(event)

        mocker.patch.object(StreamsExplorer, "setup")
        monkeypatch.setattr(StreamsExplorer, "watch", watch)

        from main import app

        update_client_full = mocker.spy(StreamsExplorer, "update_client_full")
        update_clients_delta = mocker.spy(StreamsExplorer, "_update_clients_delta")
        connect = mocker.spy(ClientManager, "connect")

        with TestClient(app) as client:
            streams_explorer = get_streams_explorer_from_state(app)

            with client.websocket_connect(WS_ENDPOINT) as ws1:
                assert connect.call_count == 1
                assert update_clients_delta.call_count == 5
                assert ws1.receive_json() == {
                    "id": "test-namespace/streaming-app1",
                    "replicas": [None, 1],
                    "state": K8sReason.UNKNOWN,
                }
                assert update_client_full.call_count == 1
                assert ws1.receive_json() == {
                    "id": "test-namespace/streaming-app2",
                    "replicas": [None, 1],
                    "state": K8sReason.STARTED,
                }
                assert ws1.receive_json() == {
                    "id": "test-namespace/streaming-app3",
                    "replicas": [None, 1],
                    "state": K8sReason.BACKOFF,
                }

                with client.websocket_connect(WS_ENDPOINT) as ws2:
                    assert connect.call_count == 2
                    for _ in range(3):  # receive full update
                        ws2.receive_json()
                    assert update_client_full.call_count == 2

                    # scale replicas
                    deployment = APP1
                    assert deployment.status
                    deployment.status.replicas = 10
                    deployment.status.ready_replicas = 0
                    update = K8sDeploymentUpdate(
                        type=K8sDeploymentUpdateType.MODIFIED, object=deployment
                    )
                    await streams_explorer.handle_deployment_update(update)
                    assert update_clients_delta.call_count == 6
                    assert (
                        ws1.receive_json()
                        == ws2.receive_json()
                        == {
                            "id": "test-namespace/streaming-app1",
                            "replicas": [0, 10],
                            "state": K8sReason.UNKNOWN,
                        }
                    )

                    # pod restarting
                    object = EventsV1Event(
                        type=K8sEventType.NORMAL,
                        reason=K8sReason.STARTED,
                        regarding=V1ObjectReference(
                            field_path="spec.containers{streaming-app3}",
                            namespace="test-namespace",
                        ),
                        event_time=datetime.datetime.now(),
                    )
                    event = K8sEvent(type=K8sEventType.NORMAL, object=object)
                    await streams_explorer.handle_event(event)
                    assert update_clients_delta.call_count == 7
                    assert (
                        ws1.receive_json()
                        == ws2.receive_json()
                        == {
                            "id": "test-namespace/streaming-app3",
                            "replicas": [None, 1],
                            "state": K8sReason.STARTED,
                        }
                    )

                    ws1.close()
                    ws2.close()

    def test_websocket_disconnect(self, mocker: MockerFixture):
        """
        Simulate client dropping connection.
        This occurs when the user closes the browser window or triggers a page refresh.
        """
        mocker.patch.object(StreamsExplorer, "setup")
        mocker.patch.object(StreamsExplorer, "watch")

        from main import app

        connect = mocker.spy(ClientManager, "connect")
        disconnect = mocker.spy(ClientManager, "disconnect")

        with TestClient(app) as client:
            streams_explorer = get_streams_explorer_from_state(app)
            with client.websocket_connect(WS_ENDPOINT) as ws:
                assert connect.call_count == 1
                assert disconnect.call_count == 0
                ws.close()  # client disconnects
                sleep(1)  # HACK: wait for coroutine disconnect to run
                assert disconnect.call_count == 1
                assert len(streams_explorer.client_manager._clients) == 0
