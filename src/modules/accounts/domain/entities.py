from dataclasses import dataclass, field

from modules.accounts.domain.value_objects import AccountId
from seedwork.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Account(AggregateRoot):
    id: AccountId = field(hash=True)
    name: str
