from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from seedwork.domain.value_objects import ValueObject

AccountId = NewType("AccountId", UUID)


@dataclass(frozen=True)
class Address(ValueObject):
    country: str
    city: str

    def __composite_values__(self) -> tuple[str, str]:
        return self.country, self.city
