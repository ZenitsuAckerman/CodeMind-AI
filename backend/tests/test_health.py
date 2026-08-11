import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Verify that the health check endpoint returns 200 OK and expected structure."""
    response = await client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data

@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Verify that the root endpoint returns basic application metadata."""
    response = await client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "CodeMind AI"
    assert data["status"] == "running"
