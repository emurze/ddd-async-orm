from uuid import UUID

from pydantic import Field

from modules.accounts.application import accounts_module
from modules.accounts.domain.entities import Account
from modules.accounts.domain.repositories import IAccountRepository
from seedwork.application.commands import Command
from seedwork.domain.services import next_id


class CreateAccountCommand(Command):
    id: UUID = Field(default_factory=next_id)
    name: str


@accounts_module.handler(CreateAccountCommand)
async def create_account(
    command: CreateAccountCommand,
    account_repository: IAccountRepository,
):
    account_repository.add(Account.model_from(command))
