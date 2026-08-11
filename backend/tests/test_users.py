import pytest
from httpx import AsyncClient
from app.config.settings import settings

API_STR = settings.API_V1_STR

@pytest.mark.asyncio
async def test_get_current_user_success(auth_client: AsyncClient, test_user: dict):
    """Test retrieving the currently authenticated user."""
    response = await auth_client.get(f"{API_STR}/users/me")
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient):
    """Test retrieving the current user without a token fails."""
    # Using the standard unauthenticated client
    response = await client.get(f"{API_STR}/users/me")
    
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: AsyncClient):
    """Test retrieving the current user with an invalid token fails."""
    client.headers["Authorization"] = "Bearer invalid.fake.token"
    response = await client.get(f"{API_STR}/users/me")
    
    # Depending on implementation this could be 401 or 403
    assert response.status_code in (401, 403)
