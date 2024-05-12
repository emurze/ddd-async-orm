from collections.abc import Callable
from uuid import UUID

from pydantic import Field

from modules.accounts.application import accounts_module
from modules.accounts.application.event import AccountCreatedEvent
from modules.accounts.domain.entities import Account
from modules.accounts.domain.repositories import IAccountRepository
from seedwork.application.commands import Command
from seedwork.application.dtos import DTO
from seedwork.domain.services import next_id


class AddressDTO(DTO):
    country: str
    city: str


class CreateAccountCommand(Command):
    id: UUID = Field(default_factory=next_id)
    name: str
    address: AddressDTO | None = None


@accounts_module.handler(CreateAccountCommand)
async def create_account(
    command: CreateAccountCommand,
    account_repository: IAccountRepository,
    publish: Callable,
) -> None:
    """
    todo: Integration event in publish?
    https://mehmetozkaya.medium.com/domain-events-in-ddd-and-domain-vs-integration-events-in-microservices-architecture-c8d92787de86
    https://medium.com/design-microservices-architecture-with-patterns/outbox-pattern-for-microservices-architectures-1b8648dfaa27
    todo: pragmatic error handling
    """
    account_repository.add(Account.from_dict(command.model_dump()))
    await publish(AccountCreatedEvent(id=command.id))
