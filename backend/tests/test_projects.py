import pytest
import uuid
from httpx import AsyncClient
from app.config.settings import settings

API_STR = settings.API_V1_STR

@pytest.fixture
def project_payload():
    return {
        "name": "Test CodeMind Project",
        "description": "An automated test project for API verification."
    }

# ==========================================
# CRUD HAPPY PATH TESTS
# ==========================================

@pytest.mark.asyncio
async def test_create_project(auth_client: AsyncClient, project_payload: dict):
    """Test successful project creation by an authenticated user."""
    response = await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == project_payload["name"]
    assert data["description"] == project_payload["description"]
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data
    assert "updated_at" in data

@pytest.mark.asyncio
async def test_list_projects(auth_client: AsyncClient, project_payload: dict):
    """Test that listing projects returns the user's created projects."""
    # Create one first
    await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    
    response = await auth_client.get(f"{API_STR}/projects/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == project_payload["name"]

@pytest.mark.asyncio
async def test_get_project(auth_client: AsyncClient, project_payload: dict):
    """Test retrieving a specific project by ID."""
    create_resp = await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    project_id = create_resp.json()["id"]
    
    response = await auth_client.get(f"{API_STR}/projects/{project_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == project_payload["name"]

@pytest.mark.asyncio
async def test_update_project(auth_client: AsyncClient, project_payload: dict):
    """Test updating a project's fields."""
    create_resp = await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    project_id = create_resp.json()["id"]
    
    update_payload = {"name": "Updated Project Name"}
    patch_resp = await auth_client.patch(f"{API_STR}/projects/{project_id}", json=update_payload)
    
    assert patch_resp.status_code == 200
    updated_data = patch_resp.json()
    assert updated_data["name"] == "Updated Project Name"
    # Description should remain unchanged
    assert updated_data["description"] == project_payload["description"]
    
    # Verify persistence
    get_resp = await auth_client.get(f"{API_STR}/projects/{project_id}")
    assert get_resp.json()["name"] == "Updated Project Name"

@pytest.mark.asyncio
async def test_delete_project(auth_client: AsyncClient, project_payload: dict):
    """Test deleting a project."""
    create_resp = await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    project_id = create_resp.json()["id"]
    
    delete_resp = await auth_client.delete(f"{API_STR}/projects/{project_id}")
    assert delete_resp.status_code == 204
    
    # Verify it is gone
    get_resp = await auth_client.get(f"{API_STR}/projects/{project_id}")
    assert get_resp.status_code == 404

# ==========================================
# OWNERSHIP AND SECURITY TESTS
# ==========================================

@pytest.mark.asyncio
async def test_security_user_b_cannot_get_user_a_project(
    auth_client: AsyncClient, 
    auth_client_b: AsyncClient, 
    project_payload: dict
):
    """Verify that User B cannot retrieve a project owned by User A."""
    # User A creates a project
    create_resp = await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    project_id = create_resp.json()["id"]
    
    # User B attempts to access it
    b_resp = await auth_client_b.get(f"{API_STR}/projects/{project_id}")
    assert b_resp.status_code in (403, 404), "SECURITY DEFECT: User B could access User A's project!"

@pytest.mark.asyncio
async def test_security_user_b_cannot_update_user_a_project(
    auth_client: AsyncClient, 
    auth_client_b: AsyncClient, 
    project_payload: dict
):
    """Verify that User B cannot modify a project owned by User A."""
    create_resp = await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    project_id = create_resp.json()["id"]
    
    update_payload = {"name": "Hacked Name"}
    b_resp = await auth_client_b.patch(f"{API_STR}/projects/{project_id}", json=update_payload)
    assert b_resp.status_code in (403, 404), "SECURITY DEFECT: User B could modify User A's project!"

@pytest.mark.asyncio
async def test_security_user_b_cannot_delete_user_a_project(
    auth_client: AsyncClient, 
    auth_client_b: AsyncClient, 
    project_payload: dict
):
    """Verify that User B cannot delete a project owned by User A."""
    create_resp = await auth_client.post(f"{API_STR}/projects/", json=project_payload)
    project_id = create_resp.json()["id"]
    
    b_resp = await auth_client_b.delete(f"{API_STR}/projects/{project_id}")
    assert b_resp.status_code in (403, 404), "SECURITY DEFECT: User B could delete User A's project!"
    
    # Verify User A's project still exists
    verify_resp = await auth_client.get(f"{API_STR}/projects/{project_id}")
    assert verify_resp.status_code == 200

# ==========================================
# VALIDATION AND EDGE CASES
# ==========================================

@pytest.mark.asyncio
async def test_unauthenticated_access_denied(client: AsyncClient, project_payload: dict):
    """Verify that unauthenticated clients cannot access project endpoints."""
    # Post
    resp = await client.post(f"{API_STR}/projects/", json=project_payload)
    assert resp.status_code == 401
    
    # Get List
    resp = await client.get(f"{API_STR}/projects/")
    assert resp.status_code == 401
    
    # Get Item
    random_id = str(uuid.uuid4())
    resp = await client.get(f"{API_STR}/projects/{random_id}")
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_get_nonexistent_project(auth_client: AsyncClient):
    """Test retrieving a project ID that does not exist."""
    random_id = str(uuid.uuid4())
    response = await auth_client.get(f"{API_STR}/projects/{random_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_malformed_uuid(auth_client: AsyncClient):
    """Test using an invalid UUID string."""
    response = await auth_client.get(f"{API_STR}/projects/invalid-uuid-string")
    assert response.status_code == 422
