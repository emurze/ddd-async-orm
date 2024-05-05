import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from collections.abc import AsyncIterator


@pytest.fixture(scope="session", autouse=True)
def _start_mappers() -> None:
    pass


@pytest.fixture(scope="function")
async def _restart_tables() -> None:
    """Cleans tables before each test."""
    async with engine.begin() as conn:
        with suppress_echo(engine):
            await conn.run_sync(Model.metadata.drop_all)
            await conn.run_sync(Model.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
async def async_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def ac(_restart_tables) -> AsyncIterator[AsyncClient]:
    """Provides a configured async test client for end-to-end tests."""
    from main import app

    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url="http://test") as ac:
            yield ac
