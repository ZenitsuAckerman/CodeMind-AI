import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from app.config.settings import settings

API_STR = settings.API_V1_STR

@pytest.fixture
def mock_gemini():
    """Mock the GeminiProvider instance in chat_service."""
    with patch("app.services.chat_service.gemini_provider") as mock:
        mock.generate_answer = AsyncMock(return_value="CodeMind uses PostgreSQL for persistent application data.")
        yield mock

@pytest.mark.asyncio
async def test_chat_success(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list, mock_gemini):
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/chat",
        json={"question": "What database does CodeMind use?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "CodeMind uses PostgreSQL for persistent application data."
    assert "citations" in data
    assert len(data["citations"]) > 0
    
    mock_gemini.generate_answer.assert_called_once()
    called_prompt = mock_gemini.generate_answer.call_args[0][0]
    assert "PostgreSQL" in called_prompt

@pytest.mark.asyncio
async def test_chat_unauthenticated(client: AsyncClient, test_project: dict):
    response = await client.post(
        f"{API_STR}/projects/{test_project['id']}/chat",
        json={"question": "What database does CodeMind use?"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_chat_project_security(auth_client_b: AsyncClient, test_project: dict):
    # User B tries to chat with User A's project
    response = await auth_client_b.post(
        f"{API_STR}/projects/{test_project['id']}/chat",
        json={"question": "What database does CodeMind use?"}
    )
    assert response.status_code in (403, 404)

@pytest.mark.asyncio
async def test_chat_context_isolation(
    auth_client: AsyncClient, 
    test_project: dict, 
    indexed_project_a_data: list, 
    indexed_project_b_data: list,
    mock_gemini
):
    """User A chats about Project A. Ensure Project B's context doesn't leak."""
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/chat",
        json={"question": "What is the secret architecture information?"}
    )
    assert response.status_code == 200
    
    # Inspect the prompt
    mock_gemini.generate_answer.assert_called_once()
    called_prompt = mock_gemini.generate_answer.call_args[0][0]
    
    # Assert Project B's secret didn't leak into the prompt
    assert "private information" not in called_prompt

@pytest.mark.asyncio
async def test_chat_gemini_failure(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list):
    """Verify behavior when Gemini provider raises an exception."""
    from fastapi import HTTPException
    
    with patch("app.services.chat_service.gemini_provider") as mock:
        mock.generate_answer = AsyncMock(side_effect=HTTPException(status_code=502, detail="Failed to communicate with Gemini API"))
        
        response = await auth_client.post(
            f"{API_STR}/projects/{test_project['id']}/chat",
            json={"question": "Test failure?"}
        )
        assert response.status_code == 502

@pytest.mark.asyncio
async def test_chat_empty_context(auth_client: AsyncClient, test_project: dict, indexed_project_a_data: list, mock_gemini):
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/chat",
        json={"question": "xyzzy nonexistent info"}
    )
    assert response.status_code == 200
    
    # Depending on reranker, this might be completely empty or just very low relevance.
    # The application proceeds to call Gemini anyway.
    mock_gemini.generate_answer.assert_called_once()
