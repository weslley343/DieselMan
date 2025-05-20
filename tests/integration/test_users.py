import pytest
from sqlalchemy import text
import asyncio
import httpx
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from app.infrastructure.db.database import Base  # ou onde está seu Base = declarative_base()
from app.infrastructure.db.deps import get_session  # depende de onde está

# Crie um engine async SQLite em memória para os testes
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(DATABASE_URL, future=True, echo=False)
TestingSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False)

# Override da dependência de sessão
from collections.abc import AsyncGenerator

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

# Substitui a dependência antes do teste
app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True)
async def clear_users_table():
    async with TestingSessionLocal() as session:
        await session.execute(text("DELETE FROM users"))
        await session.commit()
    yield

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Opcional: drop tables depois
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.anyio
async def test_create_user():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/users/", json={
            "username": "weslley",
            "email": "weslley2@example.com",
            "password": "123456"
        })
        print("Response JSON:", response.json())

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "weslley"
        assert data["email"] == "weslley2@example.com"

@pytest.mark.anyio
async def test_create_user():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/users/", json={
            "username": "weslley",
            "email": "weslley2@example.com",
            "password": "123456"
        })
        print("Response JSON:", response.json())

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "weslley"
        assert data["email"] == "weslley2@example.com"