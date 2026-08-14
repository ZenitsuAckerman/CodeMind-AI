import pytest
import uuid
import os
import subprocess
from unittest.mock import patch, MagicMock, AsyncMock
from httpx import AsyncClient
from app.config.settings import settings

API_STR = settings.API_V1_STR

def mock_subprocess_run(*args, **kwargs):
    # Mock for git clone and git rev-parse
    cmd = args[0]
    if cmd[0] == "git" and cmd[1] == "clone":
        tmp_dir = cmd[-1]
        # Create some files in the mocked repo
        os.makedirs(os.path.join(tmp_dir, "src"), exist_ok=True)
        os.makedirs(os.path.join(tmp_dir, ".git"), exist_ok=True)
        os.makedirs(os.path.join(tmp_dir, "node_modules"), exist_ok=True)

        # Valid file
        with open(os.path.join(tmp_dir, "src", "main.py"), "w") as f:
            f.write("print('hello github')")

        # README
        with open(os.path.join(tmp_dir, "README.md"), "w") as f:
            f.write("# Mock Repo")

        # Ignored dir file
        with open(os.path.join(tmp_dir, ".git", "config"), "w") as f:
            f.write("core")

        # Ignored binary
        with open(os.path.join(tmp_dir, "src", "app.exe"), "wb") as f:
            f.write(b"binary data")

        return MagicMock(returncode=0)
    elif cmd[0] == "git" and cmd[1] == "rev-parse":
        mock_result = MagicMock()
        mock_result.stdout = "a1b2c3d4e5f6g7h8i9j0"
        return mock_result
    raise subprocess.CalledProcessError(1, cmd)

def mock_subprocess_run_fail(*args, **kwargs):
    cmd = args[0]
    raise subprocess.CalledProcessError(1, cmd, stderr="Repository not found")

@pytest.fixture
def mock_git():
    with patch("subprocess.run", side_effect=mock_subprocess_run) as m:
        yield m

@pytest.fixture
def mock_git_fail():
    with patch("subprocess.run", side_effect=mock_subprocess_run_fail) as m:
        yield m

@pytest.fixture
def mock_gemini():
    with patch("app.services.chat_service.gemini_provider") as mock:
        mock.generate_answer = AsyncMock(return_value="print('hello github')")
        yield mock

@pytest.mark.asyncio
async def test_ingest_public_repository_success(auth_client: AsyncClient, test_project: dict, mock_git):
    data = {
        "repository_url": "https://github.com/owner/repo",
        "branch": "main"
    }
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/github",
        json=data
    )
    assert response.status_code == 201
    repo = response.json()
    assert repo["id"] is not None
    assert repo["project_id"] == test_project["id"]
    assert repo["repository_url"] == "https://github.com/owner/repo"
    assert repo["commit_sha"] == "a1b2c3d4e5f6g7h8i9j0"

    # Check that documents were created
    doc_response = await auth_client.get(f"{API_STR}/projects/{test_project['id']}/documents")
    assert doc_response.status_code == 200
    docs = doc_response.json()
    assert len(docs) >= 2 # main.py and README.md

    titles = [d["title"] for d in docs]
    assert "src/main.py" in titles
    assert "README.md" in titles
    assert ".git/config" not in titles
    assert "src/app.exe" not in titles

    # Check source_type
    for d in docs:
        if d["title"] in ("src/main.py", "README.md"):
            assert d.get("source_type") == "github"

@pytest.mark.asyncio
async def test_ingest_unauthenticated(client: AsyncClient, test_project: dict):
    response = await client.post(
        f"{API_STR}/projects/{test_project['id']}/github",
        json={"repository_url": "https://github.com/owner/repo"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_ingest_cross_user_isolation(auth_client_b: AsyncClient, test_project: dict, mock_git):
    # User B tries to ingest into User A's project
    response = await auth_client_b.post(
        f"{API_STR}/projects/{test_project['id']}/github",
        json={"repository_url": "https://github.com/owner/repo"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_invalid_repository_url(auth_client: AsyncClient, test_project: dict, mock_git):
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/github",
        json={"repository_url": "http://evil.com/repo"}
    )
    assert response.status_code == 400
    assert "https://github.com/" in response.json()["detail"]

@pytest.mark.asyncio
async def test_clone_failure(auth_client: AsyncClient, test_project: dict, mock_git_fail):
    response = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/github",
        json={"repository_url": "https://github.com/owner/nonexistent"}
    )
    assert response.status_code == 400
    assert "Failed to clone" in response.json()["detail"]

@pytest.mark.asyncio
async def test_e2e_github_rag_pipeline(auth_client: AsyncClient, test_project: dict, mock_git, mock_gemini):
    # 1. Ingest
    ingest_resp = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/github",
        json={"repository_url": "https://github.com/owner/rag-test-repo"}
    )
    assert ingest_resp.status_code == 201

    # 2. Get the documents created
    docs_resp = await auth_client.get(f"{API_STR}/projects/{test_project['id']}/documents")
    docs = docs_resp.json()
    assert len(docs) > 0

    # 3. Process & Index
    for d in docs:
        if d.get("source_type") == "github":
            proc_resp = await auth_client.post(f"{API_STR}/projects/{test_project['id']}/documents/{d['id']}/process")
            assert proc_resp.status_code == 202

            idx_resp = await auth_client.post(f"{API_STR}/projects/{test_project['id']}/documents/{d['id']}/index")
            assert idx_resp.status_code == 202

    # 4. Retrieval search
    search_resp = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/search",
        json={"query": "print hello github"}
    )
    assert search_resp.status_code == 200
    results = search_resp.json()["results"]
    assert len(results) > 0
    assert "hello github" in results[0]["content"]
    assert "source_type" in results[0]
    assert results[0]["source_type"] == "github"
    assert "repo_file_path" in results[0]

    # 5. Chat
    chat_resp = await auth_client.post(
        f"{API_STR}/projects/{test_project['id']}/chat",
        json={"question": "What does main.py print?"}
    )
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    assert "answer" in chat_data
    assert "citations" in chat_data
    assert len(chat_data["citations"]) > 0

    citation = chat_data["citations"][0]
    assert citation["source_type"] == "github"
    assert citation["repository_id"] is not None
    assert citation["repo_file_path"] is not None
