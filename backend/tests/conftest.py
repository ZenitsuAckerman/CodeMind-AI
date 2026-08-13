import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from alembic.config import Config
from alembic import command

from app.main import app
from app.config.settings import settings
from app.db.session import get_db
from app.db.base import Base

# --- TEST DATABASE SETUP ---

# Test Database URL configuration should be overridden via pytest.ini



from sqlalchemy import create_engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Run Alembic migrations to construct the test schema before the session.
    Clean up tables after the session completes.
    """
    # Force use the test database
    assert "test_db" in settings.DATABASE_URL
    
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    
    # Run migrations synchronously (Alembic's async support handles this under the hood via env.py)
    # Since this is a regular fixture, it runs outside the test coroutine, avoiding asyncio.run() clash.
    command.upgrade(alembic_cfg, "head")
    
    yield
    
    # Clean up using alembic downgrade instead of synchronous engine
    command.downgrade(alembic_cfg, "base")

@pytest_asyncio.fixture()
async def db_session():
    """
    Provide a transactional database session for a single test.
    Rolls back the transaction after the test to guarantee isolation.
    """
    test_engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    TestingSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )
    
    connection = await test_engine.connect()
    transaction = await connection.begin()
    
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()
    await test_engine.dispose()

@pytest.fixture()
def app_with_db_override(db_session: AsyncSession):
    """
    Provides the FastAPI app with the database dependency overridden.
    Ensures deterministic setup and teardown of the override.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()

@pytest_asyncio.fixture()
async def client(app_with_db_override):
    """
    Return an HTTPX AsyncClient configured to hit the FastAPI app,
    with the get_db dependency overridden to yield the isolated test session.
    """
    async with AsyncClient(transport=ASGITransport(app=app_with_db_override), base_url="http://test") as c:
        yield c


# --- TEST USER & AUTH SETUP ---

@pytest_asyncio.fixture()
async def test_user(client: AsyncClient):
    """Register and return a standard test user."""
    payload = {
        "email": "test@codemind.ai",
        "password": "SecurePassword123!",
        "full_name": "Test User"
    }
    response = await client.post(f"{settings.API_V1_STR}/auth/register", json=payload)
    # Registration might auto-login or just return user, so we explicitly grab a token
    return payload

@pytest_asyncio.fixture()
async def test_user_token(client: AsyncClient, test_user: dict):
    """Return a valid JWT access token for the test user."""
    response = await client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    return response.json()["access_token"]

@pytest_asyncio.fixture()
async def auth_client(test_user_token: str, app_with_db_override):
    """Return an HTTPX client pre-authenticated as the test user."""
    async with AsyncClient(transport=ASGITransport(app=app_with_db_override), base_url="http://test") as c:
        c.headers["Authorization"] = f"Bearer {test_user_token}"
        yield c

@pytest_asyncio.fixture()
async def test_user_b(client: AsyncClient):
    """Register and return a secondary test user for authorization boundary testing."""
    payload = {
        "email": "userb@codemind.ai",
        "password": "SecurePassword123!",
        "full_name": "User B"
    }
    await client.post(f"{settings.API_V1_STR}/auth/register", json=payload)
    return payload

@pytest_asyncio.fixture()
async def auth_client_b(test_user_b: dict, app_with_db_override):
    """Return an HTTPX client pre-authenticated as User B."""
    async with AsyncClient(transport=ASGITransport(app=app_with_db_override), base_url="http://test") as c:
        token_resp = await c.post(
            f"{settings.API_V1_STR}/auth/token",
            data={"username": test_user_b["email"], "password": test_user_b["password"]}
        )
        c.headers["Authorization"] = f"Bearer {token_resp.json()['access_token']}"
        yield c

# --- TEST PROJECT SETUP ---

@pytest_asyncio.fixture()
async def test_project(auth_client: AsyncClient):
    """Create and return a standard test project for User A."""
    payload = {
        "name": "Test Project A",
        "description": "Project owned by User A"
    }
    response = await auth_client.post(f"{settings.API_V1_STR}/projects/", json=payload)
    return response.json()

@pytest_asyncio.fixture()
async def test_project_b(auth_client_b: AsyncClient):
    """Create and return a standard test project for User B."""
    payload = {
        "name": "Test Project B",
        "description": "Project owned by User B"
    }
    response = await auth_client_b.post(f"{settings.API_V1_STR}/projects/", json=payload)
    return response.json()

# --- TEST DOCUMENT & RAG SETUP ---

@pytest.fixture
def sample_text_content():
    return b"CodeMind automated testing.\nThis document belongs to the test project.\nRetrieval should preserve this content."

@pytest.fixture
def sample_file(sample_text_content):
    return {"file": ("test_doc.txt", sample_text_content, "text/plain")}

@pytest.fixture
def invalid_file():
    return {"file": ("test_doc.exe", b"binary content", "application/x-msdownload")}

@pytest_asyncio.fixture()
async def test_document(auth_client: AsyncClient, test_project: dict, sample_file: dict):
    """Uploads a test document and cleans it up after."""
    data = {"title": "Test Document"}
    response = await auth_client.post(
        f"{settings.API_V1_STR}/projects/{test_project['id']}/documents",
        data=data,
        files=sample_file
    )
    assert response.status_code == 201
    doc = response.json()
    yield doc
    await auth_client.delete(f"{settings.API_V1_STR}/documents/{doc['id']}")

@pytest_asyncio.fixture()
async def processed_document(auth_client: AsyncClient, test_project: dict, test_document: dict):
    """Returns a document that has been processed."""
    response = await auth_client.post(
        f"{settings.API_V1_STR}/projects/{test_project['id']}/documents/{test_document['id']}/process"
    )
    assert response.status_code == 202
    
    get_response = await auth_client.get(f"{settings.API_V1_STR}/documents/{test_document['id']}")
    return get_response.json()

@pytest_asyncio.fixture()
async def indexed_document(auth_client: AsyncClient, test_project: dict, processed_document: dict):
    """Returns a document that has been indexed."""
    response = await auth_client.post(
        f"{settings.API_V1_STR}/projects/{test_project['id']}/documents/{processed_document['id']}/index"
    )
    assert response.status_code == 202
    
    get_response = await auth_client.get(f"{settings.API_V1_STR}/documents/{processed_document['id']}")
    return get_response.json()

@pytest_asyncio.fixture()
async def indexed_project_a_data(auth_client: AsyncClient, test_project: dict):
    """Creates specific indexed documents for RAG retrieval testing in Project A."""
    docs = []
    contents = [
        b"CodeMind uses PostgreSQL to store users and projects.",
        b"CodeMind uses Qdrant for vector similarity search.",
        b"OAuth2PasswordBearer is used for authentication."
    ]
    for i, content in enumerate(contents):
        file = {"file": (f"doc_{i}.txt", content, "text/plain")}
        data = {"title": f"Doc {i}"}
        resp = await auth_client.post(f"{settings.API_V1_STR}/projects/{test_project['id']}/documents", data=data, files=file)
        doc = resp.json()
        await auth_client.post(f"{settings.API_V1_STR}/projects/{test_project['id']}/documents/{doc['id']}/process")
        await auth_client.post(f"{settings.API_V1_STR}/projects/{test_project['id']}/documents/{doc['id']}/index")
        docs.append(doc)
    
    yield docs
    
    for doc in docs:
        await auth_client.delete(f"{settings.API_V1_STR}/documents/{doc['id']}")

@pytest_asyncio.fixture()
async def indexed_project_b_data(auth_client_b: AsyncClient, test_project_b: dict):
    """Creates specific indexed documents for RAG retrieval testing in Project B."""
    file = {"file": ("secret.txt", b"This is private information belonging to another project.", "text/plain")}
    data = {"title": "Secret B Doc"}
    resp = await auth_client_b.post(f"{settings.API_V1_STR}/projects/{test_project_b['id']}/documents", data=data, files=file)
    doc = resp.json()
    await auth_client_b.post(f"{settings.API_V1_STR}/projects/{test_project_b['id']}/documents/{doc['id']}/process")
    await auth_client_b.post(f"{settings.API_V1_STR}/projects/{test_project_b['id']}/documents/{doc['id']}/index")
    
    yield [doc]
    
    await auth_client_b.delete(f"{settings.API_V1_STR}/documents/{doc['id']}")
