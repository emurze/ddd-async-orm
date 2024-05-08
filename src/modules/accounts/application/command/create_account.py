from uuid import UUID

from pydantic import Field

from modules.accounts.application import accounts_module
from modules.accounts.domain.entities import Account
from modules.accounts.domain.events import AccountCreatedEvent
from modules.accounts.domain.repositories import IAccountRepository
from seedwork.application.commands import Command
from seedwork.domain.errors import Error
from seedwork.domain.services import next_id


class CreateAccountCommand(Command):
    id: UUID = Field(default_factory=next_id)
    name: str


@accounts_module.handler(CreateAccountCommand)
async def create_account(
    command: CreateAccountCommand,
    account_repository: IAccountRepository,
    publish,
) -> None:
    """
    todo: Integration event in publish?
    https://mehmetozkaya.medium.com/domain-events-in-ddd-and-domain-vs-integration-events-in-microservices-architecture-c8d92787de86
    https://medium.com/design-microservices-architecture-with-patterns/outbox-pattern-for-microservices-architectures-1b8648dfaa27
    todo: Value Object as serializable, composite.
    """
    print(f"{command=}")
    print(f"{publish=}")
    account_repository.add(Account.from_dict(command.model_dump()))
    publish(AccountCreatedEvent(id=command.id))
    # return Error.not_found()
