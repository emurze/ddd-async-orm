import itertools

from typing import Any, Self
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.events import DomainEvent
from seedwork.domain.repositories import IGenericRepository

from collections.abc import Iterator

from seedwork.infra.awaitable_attrs import (
    SqlAlchemyAwaitableAttrs,
    MemoryAwaitableAttrs,
    GenericAwaitableAttrs,
)


class Deleted:
    def __repr__(self) -> str:
        return "<Deleted>"


DELETED = Deleted()


class SqlAlchemyRepository(IGenericRepository[AggregateRoot]):
    entity_class: type[AggregateRoot]
    awaitable_class: type[GenericAwaitableAttrs] = SqlAlchemyAwaitableAttrs

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.identity_map: dict[UUID, Any] = {}

    def add(self, entity: AggregateRoot) -> UUID:
        self.session.add(entity)
        self.identity_map[entity.id] = entity

        if not hasattr(entity, "events"):
            entity.events = []
        if not hasattr(entity, "awaitable_attrs"):
            entity.awaitable_attrs = self.awaitable_class.wrap(entity)

        return entity.id

    async def delete(self, entity: AggregateRoot) -> None:
        await self.delete_by_id(entity.id)

    async def delete_by_id(self, entity_id: UUID) -> None:
        assert (
            self.identity_map.get(entity_id) != DELETED
        ), f"Entity {entity_id} has already been deleted."

        self.identity_map[entity_id] = DELETED
        if model := await self.session.get(self.entity_class, entity_id):
            await self.session.delete(model)

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> AggregateRoot | None:
        """
        Retrieves an entity by ID from the repository.
        Sets memory awaitable_attr for async lazy loading.
        """

        if stored_entity := self.identity_map.get(entity_id):
            return None if stored_entity is DELETED else stored_entity

        entity: Any = await self.session.get(
            self.entity_class, entity_id, with_for_update=for_update
        )
        if entity:
            entity.awaitable_attrs = self.awaitable_class.wrap(entity)
            entity.events = []
            self.identity_map[entity.id] = entity

        return entity

    async def count(self) -> int:
        query = select(func.count()).select_from(self.entity_class)
        return (await self.session.execute(query)).scalar_one()

    def collect_events(self) -> Iterator[DomainEvent]:
        return itertools.chain.from_iterable(
            entity.collect_events()
            for entity in self.identity_map.values()
            if entity is not DELETED
        )


class InMemoryRepository(IGenericRepository[AggregateRoot]):
    """
    Should always be wrapped by with
    Example:
        ```
        with InMemoryRepository(Entity):
            # Access entities here
        ```
    """

    awaitable_class: type[MemoryAwaitableAttrs] = MemoryAwaitableAttrs

    def __init__(self) -> None:
        self._old_entity_getter = None
        self.entity_class = None
        self.identity_map: dict[UUID, Any] = {}

    def add(self, entity: AggregateRoot) -> UUID:
        self.override_getattr(type(entity))
        self.identity_map[entity.id] = entity
        return entity.id

    async def delete(self, entity: AggregateRoot) -> None:
        del self.identity_map[entity.id]

    async def delete_by_id(self, entity_id: UUID) -> None:
        del self.identity_map[entity_id]

    async def count(self) -> int:
        return len(self.identity_map.values())

    def collect_events(self) -> Iterator[DomainEvent]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self.identity_map.values()
        )

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> AggregateRoot | None:
        """
        Retrieves an entity by ID from the repository.
        Sets memory awaitable_attr for async lazy loading.
        """
        if entity := self.identity_map.get(entity_id):
            entity.awaitable_attrs = self.awaitable_class.wrap(entity)
        self.override_getattr(type(entity))
        return entity

    def override_getattr(self, entity_class) -> None:
        if not self._old_entity_getter:
            self._old_entity_getter = entity_class.__getattribute__
            entity_class.__getattribute__ = self.awaitable_class.getattr
            self.entity_class = entity_class

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        if self.entity_class:
            self.entity_class.__getattribute__ = self._old_entity_getter
