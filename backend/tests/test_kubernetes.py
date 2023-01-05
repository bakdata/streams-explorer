from unittest.mock import AsyncMock, MagicMock, call

import pytest
from kubernetes_asyncio.client import ApiException, V1Deployment, V1DeploymentList
from pytest_mock import MockFixture

from streams_explorer.core.services.kubernetes import K8sResource, Kubernetes


@pytest.fixture
def kubernetes() -> Kubernetes:
    kubernetes = Kubernetes(streams_explorer=MagicMock())
    assert len(kubernetes.namespaces) == 1
    return kubernetes


@pytest.mark.asyncio
async def test_watch(kubernetes: Kubernetes, mocker: MockFixture):
    mock_kubernetes_asyncio_watch = mocker.patch(
        "streams_explorer.core.services.kubernetes.kubernetes_asyncio.watch.Watch"
    )
    mock_watch_namespace = mocker.spy(kubernetes, "_Kubernetes__watch_namespace")

    mock_Watch = AsyncMock(side_effect=ApiException(status=410, reason="Expired"))

    mock_kubernetes_asyncio_watch.return_value = mock_Watch
    # mock_Watch.__aenter__.side_effect = ApiException(status=410, reason="Expired")

    await kubernetes.watch()

    assert mock_kubernetes_asyncio_watch.call_count == 3
    assert mock_kubernetes_asyncio_watch.call_args_list == [
        call("V1Deployment"),
        call("V1StatefulSet"),
        call("V1beta1CronJob"),
    ]
    mock_Watch.__aenter__.assert_awaited()
    assert mock_Watch.__aenter__.await_count == 3

    assert mock_watch_namespace.call_count == 4
    resources: list[str] = [
        call.args[1].return_type.__name__
        for call in mock_watch_namespace.call_args_list
    ]
    assert resources == [
        "V1Deployment",
        "V1StatefulSet",
        "V1beta1CronJob",
        "EventsV1Event",
    ]


@pytest.mark.asyncio
async def test_watch_namespace(kubernetes: Kubernetes, mocker: MockFixture):
    mock_kubernetes_asyncio_watch = mocker.patch(
        "streams_explorer.core.services.kubernetes.kubernetes_asyncio.watch.Watch.stream"
    )
    mock_watch_namespace = mocker.spy(kubernetes, "_Kubernetes__watch_namespace")

    mock_Watch = AsyncMock()
    mock_kubernetes_asyncio_watch.return_value = mock_Watch
    mock_Watch.__aenter__.return_value.stream.return_value.__aenter__.return_value = []

    def mock_list_deployments() -> V1DeploymentList:
        return V1DeploymentList()

    async def mock_callback() -> None:
        pass

    await mock_watch_namespace(
        "test-namespace",
        K8sResource(
            mock_list_deployments, return_type=V1Deployment, callback=mock_callback
        ),
    )

    assert mock_kubernetes_asyncio_watch.call_count == 1


@pytest.mark.asyncio
async def test_watch_namespace_error(kubernetes: Kubernetes, mocker: MockFixture):
    mock_kubernetes_asyncio_watch = mocker.patch(
        "streams_explorer.core.services.kubernetes.kubernetes_asyncio.watch.Watch"
    )
    mock_watch_namespace = mocker.spy(kubernetes, "_Kubernetes__watch_namespace")

    mock_Watch = AsyncMock()
    mock_kubernetes_asyncio_watch.return_value = mock_Watch
    mock_Watch.__aenter__.side_effect = ApiException(
        status=500, reason="Internal Server Error"
    )

    def mock_list_deployments() -> V1DeploymentList:
        return V1DeploymentList()

    async def mock_callback() -> None:
        pass

    with pytest.raises(ApiException) as e:
        await mock_watch_namespace(
            "test-namespace",
            K8sResource(
                mock_list_deployments, return_type=None, callback=mock_callback
            ),
        )
        assert e.value.status == 500
        assert e.value.reason == "Internal Server Error"


@pytest.mark.asyncio
async def test_watch_namespace_restart(kubernetes: Kubernetes, mocker: MockFixture):
    mock_kubernetes_asyncio_watch = mocker.patch(
        "streams_explorer.core.services.kubernetes.kubernetes_asyncio.watch.Watch"
    )
    mock_watch_namespace = mocker.spy(kubernetes, "_Kubernetes__watch_namespace")

    mock_Watch = AsyncMock()
    mock_kubernetes_asyncio_watch.return_value = mock_Watch
    mock_Watch.__aenter__.side_effect = ApiException(status=410, reason="Expired")

    def mock_list_deployments() -> V1DeploymentList:
        return V1DeploymentList()

    async def mock_callback() -> None:
        pass

    with pytest.raises(RecursionError):
        await mock_watch_namespace(
            "test-namespace",
            K8sResource(
                mock_list_deployments, return_type=None, callback=mock_callback
            ),
        )

    # assert mock_kubernetes_asyncio_watch.call_count == 1
    # assert mock_kubernetes_asyncio_watch.call_args_list == [call("V1Deployment")]
