from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import registry

base_registry = registry()


@contextmanager
def suppress_echo(engine: AsyncEngine) -> Generator:
    engine.echo = False
    yield
    engine.echo = True
