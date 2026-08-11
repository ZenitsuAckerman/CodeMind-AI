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

@pytest_asyncio.fixture()
async def client(db_session: AsyncSession):
    """
    Return an HTTPX AsyncClient configured to hit the FastAPI app,
    with the get_db dependency overridden to yield the isolated test session.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
        
    # Clear overrides
    app.dependency_overrides.clear()


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
async def auth_client(client: AsyncClient, test_user_token: str):
    """Return an HTTPX client pre-authenticated as the test user."""
    client.headers["Authorization"] = f"Bearer {test_user_token}"
    return client

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
async def auth_client_b(test_user_b: dict, db_session: AsyncSession):
    """Return an HTTPX client pre-authenticated as User B."""
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        token_resp = await c.post(
            f"{settings.API_V1_STR}/auth/token",
            data={"username": test_user_b["email"], "password": test_user_b["password"]}
        )
        c.headers["Authorization"] = f"Bearer {token_resp.json()['access_token']}"
        yield c
        
    app.dependency_overrides.clear()
