import pytest
from sqlalchemy import select

from modules.accounts.application.command import (
    CreateAccountCommand,
    AddressDTO,
)
from modules.accounts.application.command.create_account import create_account
from modules.accounts.application.query import GetAccountQuery
from modules.accounts.domain.repositories import IAccountRepository
from seedwork.application.application import Application
from seedwork.application.inbox_outbox import OutboxMessage, EventWorker
from seedwork.domain.services import next_id
from seedwork.infra.inbox_outbox import SqlAlchemyMessageOutbox
from seedwork.tests.application.utils import FakeEventPublisher


@pytest.mark.unit
async def test_mem_create_account(mem_repo: IAccountRepository) -> None:
    # arrange
    account_id = next_id()
    command = CreateAccountCommand(id=account_id, name="Vlados335")
    publish = FakeEventPublisher()

    # act
    await create_account(command, mem_repo, publish)

    # assert
    account = await mem_repo.get_by_id(account_id)
    assert account.name == "Vlados335"
    assert publish.contains("AccountCreatedEvent")


@pytest.mark.marked
@pytest.mark.integration
async def test_sqlalchemy_create_account(app: Application, db_session) -> None:
    # arrange
    account_id = next_id()
    address = AddressDTO(country="Russian", city="Moscow")
    command = CreateAccountCommand(
        id=account_id,
        name="Vlados335",
        address=address,
    )
    await app.execute_async(command)

    res = await db_session.execute(select(OutboxMessage))
    assert len(res.scalars().all()) == 1

    worker = EventWorker(app, SqlAlchemyMessageOutbox)
    await worker.process_outbox_message()

    query = GetAccountQuery(id=account_id)
    res = await app.execute_async(query)
    print(f"{res.payload}")
