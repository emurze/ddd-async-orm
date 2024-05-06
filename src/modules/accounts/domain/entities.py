from modules.accounts.domain.value_objects import AccountId
from seedwork.domain.entities import AggregateRoot


class Account(AggregateRoot):
    id: AccountId
    name: str
