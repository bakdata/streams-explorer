from unittest.mock import AsyncMock, MagicMock

import pytest
from kubernetes_asyncio.client import ApiException
from pytest_mock import MockFixture

from streams_explorer.core.services.kubernetes import Kubernetes


@pytest.fixture
def kubernetes() -> Kubernetes:
    kubernetes = Kubernetes(streams_explorer=MagicMock())
    assert len(kubernetes.namespaces) == 1
    return kubernetes


@pytest.mark.asyncio
async def test_watch(kubernetes: Kubernetes, mocker: MockFixture):
    mock_kubernetes_asyncio_watch = mocker.patch(
        "streams_explorer.core.services.kubernetes.Watch"
    )
    mock_watch_namespace = mocker.spy(kubernetes, "_Kubernetes__watch_namespace")

    mock_ctx = AsyncMock(side_effect=ApiException(status=410))
    mock_kubernetes_asyncio_watch.return_value = mock_ctx
    await kubernetes.watch()
    mock_kubernetes_asyncio_watch.assert_called()
    mock_ctx.__aenter__.assert_awaited()
    assert mock_ctx.__aenter__.await_count == 3
    assert mock_watch_namespace.call_count == 4
