import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from modules.accounts.infra.repositories import AccountSqlAlchemyRepository


@pytest.mark.integration
async def test_account_repo_is_empty(db_session: AsyncSession) -> None:
    repo = AccountSqlAlchemyRepository(db_session)
    assert await repo.count() == 0
