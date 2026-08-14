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
    
    # Verify it is gone from DB
    get_resp = await auth_client.get(f"{API_STR}/documents/{doc['id']}")
    assert get_resp.status_code == 404
    
    # We didn't index this doc, so Qdrant check is trivial here. Let's rely on the dedicated tests below.

@pytest.mark.asyncio
async def test_delete_document_removes_qdrant_vectors(auth_client: AsyncClient, test_project: dict, indexed_document: dict):
    from app.services.rag.qdrant_service import qdrant_service
    from qdrant_client.http.models import Filter, FieldCondition, MatchValue
    
    doc_id = indexed_document["id"]
    proj_id = test_project["id"]
    
    # Verify vectors exist in Qdrant first
    res = qdrant_service.client.scroll(
        collection_name=qdrant_service.collection_name,
        scroll_filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=str(doc_id)))]),
        limit=10
    )
    assert len(res[0]) > 0, "Vectors should exist before deletion"
    
    # Delete document
    del_resp = await auth_client.delete(f"{API_STR}/documents/{doc_id}")
    assert del_resp.status_code == 204
    
    # Verify vectors are gone
    res_after = qdrant_service.client.scroll(
        collection_name=qdrant_service.collection_name,
        scroll_filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=str(doc_id)))]),
        limit=10
    )
    assert len(res_after[0]) == 0, "Vectors should be deleted"

@pytest.mark.asyncio
async def test_deleted_document_invisible_to_rag(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    # Retrieve a query that we know matches Document 0
    doc_to_delete = indexed_project_a_data[0]
    
    search_payload = {"query": "PostgreSQL", "limit": 5}
    res_before = await auth_client.post(f"{API_STR}/projects/{test_project['id']}/search", json=search_payload)
    assert res_before.status_code == 200
    assert any(chunk["document_id"] == doc_to_delete["id"] for chunk in res_before.json()["results"]), "Chunk must be found before deletion"
    
    # Delete Document 0
    del_resp = await auth_client.delete(f"{API_STR}/documents/{doc_to_delete['id']}")
    assert del_resp.status_code == 204
    
    # RAG Search again
    res_after = await auth_client.post(f"{API_STR}/projects/{test_project['id']}/search", json=search_payload)
    assert res_after.status_code == 200
    assert not any(chunk["document_id"] == doc_to_delete["id"] for chunk in res_after.json()["results"]), "Deleted chunk must not be returned"

@pytest.mark.asyncio
async def test_delete_document_cross_document_isolation(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    from app.services.rag.qdrant_service import qdrant_service
    from qdrant_client.http.models import Filter, FieldCondition, MatchValue
    
    doc_a = indexed_project_a_data[0]
    doc_b = indexed_project_a_data[1]
    
    # Delete Document A
    await auth_client.delete(f"{API_STR}/documents/{doc_a['id']}")
    
    # Verify Document B vectors remain
    res_b = qdrant_service.client.scroll(
        collection_name=qdrant_service.collection_name,
        scroll_filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=str(doc_b['id'])))]),
        limit=10
    )
    assert len(res_b[0]) > 0, "Document B vectors must remain intact"

@pytest.mark.asyncio
async def test_delete_document_qdrant_failure_aborts_db_deletion(auth_client: AsyncClient, test_project: dict, indexed_document: dict):
    from unittest.mock import patch
    doc_id = indexed_document["id"]
    
    # Mock QdrantService to throw an error
    with patch("app.services.rag.qdrant_service.QdrantService.delete_document_vectors", side_effect=Exception("Simulated Qdrant failure")):
        import pytest
        with pytest.raises(Exception, match="Simulated Qdrant failure"):
            await auth_client.delete(f"{API_STR}/documents/{doc_id}")
        
    # Verify the document STILL exists in Postgres because the deletion was aborted
    get_resp = await auth_client.get(f"{API_STR}/documents/{doc_id}")
    assert get_resp.status_code == 200

@pytest.mark.asyncio
async def test_delete_document_cross_user(auth_client_b: AsyncClient, test_document: dict):
    # User B tries to delete User A's document
    response = await auth_client_b.delete(f"{API_STR}/documents/{test_document['id']}")
    assert response.status_code in (403, 404)
