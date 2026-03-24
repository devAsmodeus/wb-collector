"""Test system endpoints."""
import pytest
from litestar.testing import AsyncTestClient


@pytest.mark.anyio
async def test_health_endpoint(client: AsyncTestClient):
    """GET /health returns ok status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
