import pytest
from httpx import AsyncClient
from app.config.settings import settings

API_STR = settings.API_V1_STR

@pytest.mark.asyncio
async def test_semantic_retrieval(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    """Test semantic search with phrasing different from source."""
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/search",
        json={"query": "Which database is responsible for persistent storage?", "limit": 2}
    )
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) > 0
    # Semantic match
    assert any("PostgreSQL" in r["content"] for r in results)
    
@pytest.mark.asyncio
async def test_bm25_retrieval(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    """Test BM25 search using specific terminology."""
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/search",
        json={"query": "OAuth2PasswordBearer", "limit": 2}
    )
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) > 0
    assert any("OAuth2PasswordBearer" in r["content"] for r in results)

@pytest.mark.asyncio
async def test_deduplication(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    """Test that chunks retrieved by both vector and BM25 are deduplicated."""
    # A query that should hit both BM25 and Semantic search strongly
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/search",
        json={"query": "OAuth2PasswordBearer authentication", "limit": 10}
    )
    assert response.status_code == 200
    results = response.json()["results"]
    
    # Extract unique chunk IDs
    chunk_ids = [r["chunk_id"] for r in results]
    assert len(chunk_ids) == len(set(chunk_ids)), "Duplicate chunk IDs found in retrieval results"

@pytest.mark.asyncio
async def test_reranking_and_top_k(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    """Test that the top_k/limit parameter is respected after reranking."""
    limit = 2
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/search",
        json={"query": "database storage search authentication", "limit": limit}
    )
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) <= limit
    assert len(results) > 0

@pytest.mark.asyncio
async def test_retrieval_project_isolation(
    auth_client: AsyncClient, 
    test_project: dict, 
    indexed_project_a_data: list, 
    indexed_project_b_data: list
):
    """User A queries Project A for content that only exists in Project B."""
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/search",
        json={"query": "This is private information belonging to another project", "limit": 5}
    )
    assert response.status_code == 200
    results = response.json()["results"]
    
    # Project B's content must NOT appear
    b_doc_id = indexed_project_b_data[0]["id"]
    for r in results:
        assert "private information" not in r["content"]
        assert r["document_id"] != b_doc_id

@pytest.mark.asyncio
async def test_retrieval_no_results(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    """Query for a highly specific random string that shouldn't match anything well."""
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/search",
        json={"query": "xyzzyspoon12349876", "limit": 5}
    )
    assert response.status_code == 200
    assert "results" in response.json()
