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

- **LLM and RAG Services**: External services such as Gemini, Hugging Face, Qdrant, and GitHub are excluded from this initial regression suite. Testing these requires sophisticated mocking of boundary dependencies or dedicated integration test pipelines which have not yet been implemented.
- **Documents & Chat**: The test suite currently focuses on the structural Core (Users, Auth, Projects). Documents and chat endpoints rely on RAG infrastructure and are deferred to future integration suites.

## Security & Authorization

CodeMind strictly enforces Resource Ownership Authorization at the service layer.
- A project belongs to exactly one user via `project.owner_id`.
- The `ProjectService` validates that `project.owner_id == current_user.id` on every `GET`, `PATCH`, and `DELETE` operation.
- Cross-user access (e.g. User B attempting to mutate User A's project) is automatically rejected with a `403 Forbidden` response.
- These ownership boundaries are actively verified by the automated test suite in `tests/test_projects.py`.

*(Note: An earlier test framework bug incorrectly reported a cross-user vulnerability due to shared HTTPX client sessions mutating headers. This testing defect was resolved, confirming the underlying `ProjectService` architecture was correctly enforcing boundaries.)*
