import uuid
from typing import Any
from uuid import UUID

import pytest
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from sqlalchemy.ext.asyncio import AsyncSession

from config.provider import ContainerProvider
from modules.accounts.infra.repositories import AccountRepository


class TransactionContainer(DeclarativeContainer):  # Unit Of Work
    correlation_id = Dependency(instance_of=UUID)
    db_session = Dependency(instance_of=AsyncSession)
    account_repository: Any = Singleton(AccountRepository, session=db_session)


@pytest.mark.unit
def test_can_get_dependency() -> None:
    container_provider = ContainerProvider(
        TransactionContainer(
            correlation_id=uuid.uuid4(),
            db_session=AsyncSession(),
        )
    )
    print(container_provider.has_dependency("account_repository"))
    print(container_provider.resolve_func_params())
