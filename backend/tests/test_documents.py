import pytest
import os
from httpx import AsyncClient
from app.config.settings import settings
from app.models.document import DocumentStatus

API_STR = settings.API_V1_STR

# --- TESTS ---

@pytest.mark.asyncio
async def test_upload_document_success(auth_client: AsyncClient, test_project: dict, sample_file: dict):
    data = {"title": "My Uploaded Doc"}
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/documents",
        data=data,
        files=sample_file
    )
    assert response.status_code == 201
    doc = response.json()
    assert doc["id"] is not None
    assert doc["project_id"] == test_project["id"]
    assert doc["title"] == "My Uploaded Doc"
    assert doc["original_filename"] == "test_doc.txt"
    assert doc["status"] == "UPLOADED"
    
    # Clean up
    await auth_client.delete(f"{API_STR}/documents/{doc['id']}")

@pytest.mark.asyncio
async def test_upload_document_invalid_extension(auth_client: AsyncClient, test_project: dict, invalid_file: dict):
    data = {"title": "Invalid Doc"}
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/documents",
        data=data,
        files=invalid_file
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_upload_unauthenticated_access_denied(client: AsyncClient, test_project: dict, sample_file: dict):
    data = {"title": "Unauth Doc"}
    response = await client.post(
        f"{API_STR}/projects/{test_project['id']}/documents",
        data=data,
        files=sample_file
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_upload_document_cross_user(auth_client_b: AsyncClient, test_project: dict, sample_file: dict):
    # User B tries to upload to User A's project
    data = {"title": "Hacked Doc"}
    response = await auth_client_b.post(
        f"{API_STR}/projects/{test_project['id']}/documents",
        data=data,
        files=sample_file
    )
    assert response.status_code in (403, 404)

@pytest.mark.asyncio
async def test_list_documents(auth_client: AsyncClient, test_project: dict, test_document: dict):
    response = await auth_client.get(f"{API_STR}/projects/{test_project['id']}/documents")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 1
    assert any(d["id"] == test_document["id"] for d in docs)

@pytest.mark.asyncio
async def test_list_documents_cross_user(auth_client_b: AsyncClient, test_project: dict):
    # User B tries to list User A's documents
    response = await auth_client_b.get(f"{API_STR}/projects/{test_project['id']}/documents")
    assert response.status_code in (403, 404)

@pytest.mark.asyncio
async def test_get_document(auth_client: AsyncClient, test_document: dict):
    response = await auth_client.get(f"{API_STR}/documents/{test_document['id']}")
    assert response.status_code == 200
    doc = response.json()
    assert doc["id"] == test_document["id"]

@pytest.mark.asyncio
async def test_get_document_cross_user(auth_client_b: AsyncClient, test_document: dict):
    # User B tries to get User A's document
    response = await auth_client_b.get(f"{API_STR}/documents/{test_document['id']}")
    assert response.status_code in (403, 404)

@pytest.mark.asyncio
async def test_get_nonexistent_document(auth_client: AsyncClient):
    import uuid
    response = await auth_client.get(f"{API_STR}/documents/{uuid.uuid4()}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_process_document_success(auth_client: AsyncClient, test_project: dict, test_document: dict):
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/documents/{test_document['id']}/process"
    )
    assert response.status_code == 202
    
    # Verify status changed to PROCESSED
    doc_resp = await auth_client.get(f"{API_STR}/documents/{test_document['id']}")
    assert doc_resp.status_code == 200
    doc = doc_resp.json()
    assert doc["status"] == "PROCESSED"
    
    # The application currently does not expose the raw DocumentContent via the API,
    # but we know it should have created it. The status change implies success.

@pytest.mark.asyncio
async def test_process_document_cross_user(auth_client_b: AsyncClient, test_project: dict, test_document: dict):
    # User B tries to process User A's document
    response = await auth_client_b.post(
        f"{API_STR}/projects/{test_project['id']}/documents/{test_document['id']}/process"
    )
    assert response.status_code in (403, 404)

@pytest.mark.asyncio
async def test_index_document_success(auth_client: AsyncClient, test_project: dict, processed_document: dict):
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/documents/{processed_document['id']}/index"
    )
    assert response.status_code == 202
    
    # Verify status changed to INDEXED
    doc_resp = await auth_client.get(f"{API_STR}/documents/{processed_document['id']}")
    assert doc_resp.status_code == 200
    doc = doc_resp.json()
    assert doc["status"] == "INDEXED"

@pytest.mark.asyncio
async def test_index_unprocessed_document_fails(auth_client: AsyncClient, test_project: dict, test_document: dict):
    # Attempt to index a document that is only UPLOADED
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/documents/{test_document['id']}/index"
    )
    assert response.status_code == 400
    assert "PROCESSED" in response.json()["detail"]

@pytest.mark.asyncio
async def test_index_document_cross_user(auth_client_b: AsyncClient, test_project: dict, processed_document: dict):
    # User B tries to index User A's document
    response = await auth_client_b.post(
        f"{API_STR}/projects/{test_project['id']}/documents/{processed_document['id']}/index"
    )
    assert response.status_code in (403, 404)

@pytest.mark.asyncio
async def test_delete_document_success(auth_client: AsyncClient, test_project: dict, sample_file: dict):
    # Setup: Create a new document just to delete it
    data = {"title": "Doc to delete"}
    resp = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/documents",
        data=data,
        files=sample_file
    )
    doc = resp.json()
    
    # Delete the document
    del_resp = await auth_client.delete(f"{API_STR}/documents/{doc['id']}")
    assert del_resp.status_code == 204
    
    # Verify it is gone
    get_resp = await auth_client.get(f"{API_STR}/documents/{doc['id']}")
    assert get_resp.status_code == 404
    
    # NOTE: The architecture audit identified a known issue where deleting a document
    # does NOT remove the orphaned Qdrant vectors. We document it here but do not 
    # fail the test for it since it's an existing limitation of the application.

@pytest.mark.asyncio
async def test_delete_document_cross_user(auth_client_b: AsyncClient, test_document: dict):
    # User B tries to delete User A's document
    response = await auth_client_b.delete(f"{API_STR}/documents/{test_document['id']}")
    assert response.status_code in (403, 404)
