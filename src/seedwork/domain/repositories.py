import abc
from collections.abc import Iterator
from typing import TypeVar, Generic, Any
from uuid import UUID

from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent

T = TypeVar("T", bound=Entity)
M = TypeVar("M", bound=Any)


class IGenericRepository(Generic[T], metaclass=abc.ABCMeta):
    identity_map: dict[UUID, Any]

    @abc.abstractmethod
    def add(self, entity: T) -> UUID: ...

    @abc.abstractmethod
    async def delete(self, entity: T) -> None: ...

    @abc.abstractmethod
    async def delete_by_id(self, entity_id: UUID) -> None: ...

    @abc.abstractmethod
    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> T | None: ...

    @abc.abstractmethod
    async def count(self) -> int: ...

    @abc.abstractmethod
    def collect_events(self) -> Iterator[DomainEvent]: ...
