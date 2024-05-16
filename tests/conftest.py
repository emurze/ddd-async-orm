import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import clear_mappers
from collections.abc import AsyncIterator

from container import app_container, create_application
from seedwork.application.application import Application
from seedwork.infra.database import suppress_echo, base_registry
from seedwork.infra.repository import InMemoryRepository
from tests.config import get_test_config

config = get_test_config()
engine = create_async_engine(
    config.db_dsn, echo=config.db_echo, poolclass=NullPool
)
session_factory = async_sessionmaker(engine, expire_on_commit=True)
app_container.config.override(config)
app_container.db_engine.override(engine)


@pytest.fixture(scope="function")
async def _restart_engine() -> None:
    """Cleans tables before each test."""
    async with engine.begin() as conn:
        with suppress_echo(engine):
            await conn.run_sync(base_registry.metadata.drop_all)
            await conn.run_sync(base_registry.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
def app(_restart_engine) -> Application:
    """Restarts mappers."""
    yield create_application(config, engine)
    clear_mappers()


@pytest.fixture(scope="function")
async def db_session(app) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def ac(_restart_engine) -> AsyncIterator[AsyncClient]:
    """Provides a configured async test client for end-to-end tests."""
    from main import app as api_app

    async with LifespanManager(api_app):
        async with AsyncClient(app=api_app, base_url="http://test") as ac:
            yield ac


@pytest.fixture(scope="function")
def mem_repo() -> InMemoryRepository:
    with InMemoryRepository() as repo:
        yield repo
