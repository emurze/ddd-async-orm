import pytest

from modules.accounts.application.command import CreateAccountCommand
from modules.accounts.application.command.create_account import create_account
from modules.accounts.domain.repositories import IAccountRepository
from seedwork.domain.services import next_id
from seedwork.tests.application.utils import FakeEventPublisher


@pytest.mark.unit
async def test_create_account(mem_repo: IAccountRepository) -> None:
    # arrange
    account_id = next_id()
    command = CreateAccountCommand(
        id=account_id,
        name="Vlados335"
    )
    publish = FakeEventPublisher()

    # act
    await create_account(command, mem_repo, publish)

    # assert
    account = await mem_repo.get_by_id(account_id)
    assert account.name == "Vlados335"
    assert publish.contains("AccountCreatedEvent")
