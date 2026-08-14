# CodeMind Backend Testing Infrastructure

This document outlines the automated API testing infrastructure for the CodeMind backend. 

The test suite provides a deterministic regression safety net for authentication, user management, and project operations using `pytest`, `pytest-asyncio`, and `httpx`.

## Dependencies

Testing dependencies are isolated in `requirements-dev.txt` to prevent production bloat.
- `pytest` (Test runner)
- `pytest-asyncio` (Async execution)
- `pytest-env` (Environment variable injection)
- `httpx` (Async HTTP client)

*Note on bcrypt*: Due to a known issue with `passlib` attempting to trigger a bug-check with long passwords, the testing environment uses `bcrypt==3.2.2`. Newer versions of `bcrypt` explicitly raise exceptions during `passlib` initialization which fails the test suite setup.

## Test Database Configuration

The test suite **NEVER** mutates the normal development database (`codemind_db`). 

It connects to an isolated PostgreSQL database:
`codemind_test_db`

The database URL is automatically injected via `pytest-env` in `pytest.ini`. It inherits the existing PostgreSQL role and credentials (e.g. `rahulrio@localhost:5432`).

### Setup and Migrations
The database schema is dynamically generated at the beginning of the test session using Alembic programmatic API (`alembic.command.upgrade`). At the end of the session, the schema is rolled back (`command.downgrade("base")`) to leave the test database completely clean.

Tests use an overridden `get_db` FastAPI dependency to ensure that API requests interact exclusively with `codemind_test_db`.

## Running the Suite

Install testing dependencies:
```bash
pip install -r requirements-dev.txt
```

Run all tests:
```bash
pytest -v
```

Run specific test files:
```bash
pytest tests/test_projects.py -v
```

Run a single test:
```bash
pytest tests/test_auth.py::test_login_json_success -v
```

## What is Mocked / Excluded

- **LLM Services**: External services such as Gemini and GitHub are excluded from this regression suite.
- **Chat**: Chat endpoints rely on RAG LLM infrastructure and are deferred to future integration suites.

## Security & Authorization

CodeMind strictly enforces Resource Ownership Authorization at the service layer.
- A project belongs to exactly one user via `project.owner_id`.
- The `ProjectService` validates that `project.owner_id == current_user.id` on every `GET`, `PATCH`, and `DELETE` operation.
- Cross-user access (e.g. User B attempting to mutate User A's project) is automatically rejected with a `403 Forbidden` response.
- These ownership boundaries are actively verified by the automated test suite in `tests/test_projects.py`.

*(Note: An earlier test framework bug incorrectly reported a cross-user vulnerability due to shared HTTPX client sessions mutating headers. This testing defect was resolved, confirming the underlying `ProjectService` architecture was correctly enforcing boundaries.)*

## Document Testing

The document testing suite (`tests/test_documents.py`) provides end-to-end coverage of the document lifecycle without relying on external network dependencies:

- **Upload Tests**: Validates file extension checking, successful storage, and unauthenticated/cross-user rejection.
- **Processing Tests**: Validates the transition to `PROCESSED` status and the creation of `DocumentContent` using local text extraction.
- **Indexing Tests**: Validates chunking, embedding generation using local Hugging Face sentence transformers, and insertion into Qdrant.
- **Ownership Tests**: Strict isolation between User A and User B is tested at every step (list, get, process, index, delete).
- **File Cleanup**: Uploaded test files are cleaned up either via explicit teardown fixtures or by successfully hitting the `DELETE` endpoint. Document deletion now properly cascades to remove associated vectors from Qdrant.

### Qdrant Testing Strategy

To test the indexing pipeline deterministically without requiring a real external Qdrant instance, the suite leverages Qdrant's `:memory:` storage backend. When the application initializes the `QdrantService`, it seamlessly uses this in-memory database during tests.

### Known Limitations

*(No current major architectural limitations known in the testing suite.)*

## RAG Testing

The RAG testing suite (`tests/test_rag.py`) exercises the complete retrieval pipeline:

- **Semantic Retrieval**: Validates that Qdrant returns semantically relevant chunks.
- **BM25 Retrieval**: Validates that exact keyword terminology returns the correct chunks.
- **Deduplication**: Ensures that chunks found by both vector search and keyword search are merged and deduplicated.
- **Reranking**: Validates that the CrossEncoder reranker respects the `limit` / `top_k` parameter.
- **Project Isolation**: A critical security invariant. The tests explicitly assert that User B querying Project A cannot retrieve Project B's chunks.
- **Qdrant In-Memory**: Tests run fully deterministically without an external Qdrant cluster.

## Chat Testing

The Chat testing suite (`tests/test_chat.py`) evaluates the conversational LLM integration:

- **Gemini Mocking**: The external `GeminiProvider` boundary is mocked to return deterministic, predefined responses during normal regression tests. This prevents network latency, flakiness, and unauthorized API calls.
- **Context Isolation**: Explicitly asserts that the prompt constructed by `PromptBuilder` does not leak information from unauthorized projects.
- **Provider Failure Testing**: Mocks Gemini to raise a `502 Bad Gateway` to verify the application fails gracefully.
- **Authentication**: Verifies the endpoint rejects unauthorized requests with a `401 Unauthorized`.
- **Citations**: Asserts that the chat response successfully returns chunk indices and document UUIDs.

## Newly Discovered Production Defect (RAG Retrieval Pipeline Broken)

During the implementation of the RAG and Chat test suite, a critical production defect was discovered:
- **Defect**: The application's `QdrantService.search()` method invokes `self.client.search(...)`. However, in modern versions of the `qdrant-client` SDK (v1.11.0+), the `.search()` method has been removed and replaced by `.query_points()`.
- **Impact**: Any invocation of the RAG retrieval pipeline (both the Search and Chat endpoints) immediately crashes with an `AttributeError: 'QdrantClient' object has no attribute 'search'`.
- **Test Status**: In adherence to strict testing protocols, this defect was **not** silently patched. The 10 associated RAG and Chat tests currently fail, exposing this critical production bug. This must be addressed in a subsequent engineering sprint by migrating `QdrantService` to use `query_points()`.
