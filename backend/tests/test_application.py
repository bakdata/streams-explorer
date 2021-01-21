import pytest
from fastapi import status
from fastapi.testclient import TestClient

from streams_explorer.application import get_application


class TestApplication:
    @pytest.fixture()
    def client(self) -> TestClient:
        app = get_application()
        return TestClient(app)

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
