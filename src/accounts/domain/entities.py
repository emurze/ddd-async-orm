from dataclasses import dataclass, field

from result import Result, Err, Ok

from accounts.domain.value_objects import AccountId, Address
from seedwork.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Account(AggregateRoot):
    id: AccountId = field(hash=True)
    name: str
    address: Address | None

    def change_name(self, value: str) -> Result:
        if self.address is None:
            return Err("To change the name address should be specified.")
        self.name = value
        return Ok(None)

    def get_name_card(self) -> Result:
        if self.address is None:
            return Err("To get name card address should be specified.")
        return Ok(f"{self.name}-{self.address}")
