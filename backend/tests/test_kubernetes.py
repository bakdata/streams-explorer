from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

from streams_explorer.core.services.kubernetes import Kubernetes


@pytest.fixture
def kubernetes() -> Kubernetes:
    return Kubernetes(streams_explorer=MagicMock())


@pytest.mark.asyncio
async def test_watch(kubernetes: Kubernetes, mocker: MockFixture):
    mock_watch_namespace = mocker.patch.object(
        kubernetes, "_Kubernetes__watch_namespace"
    )
    await kubernetes.watch()
    assert mock_watch_namespace.call_count == 4
