import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from collections.abc import AsyncIterator

from sqlalchemy.orm import clear_mappers

from config.api_config import get_test_config
from config.container import create_application, override_container
from seedwork.application.application import Application
from seedwork.infra.database import suppress_echo, base_registry
from seedwork.infra.repository import InMemoryRepository

config = get_test_config()
engine = create_async_engine(
    config.db_dsn, echo=config.db_echo, poolclass=NullPool
)
session_factory = async_sessionmaker(engine, expire_on_commit=True)
override_container(config, engine)


@pytest.fixture(scope="function")
def app() -> Application:
    """Starts sqlalchemy mappers."""
    yield create_application(config, engine)
    clear_mappers()


@pytest.fixture(scope="function")
async def _restart_tables() -> None:
    """Cleans tables before each test."""
    async with engine.begin() as conn:
        with suppress_echo(engine):
            await conn.run_sync(base_registry.metadata.drop_all)
            await conn.run_sync(base_registry.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
def mem_repo() -> InMemoryRepository:
    with InMemoryRepository() as repo:
        yield repo


@pytest.fixture(scope="function")
async def db_session(app, _restart_tables) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def ac(_restart_tables) -> AsyncIterator[AsyncClient]:
    """Provides a configured async test client for end-to-end tests."""
    from api.main import app as api_app

    async with LifespanManager(api_app):
        async with AsyncClient(app=api_app, base_url="http://test") as ac:
            yield ac
