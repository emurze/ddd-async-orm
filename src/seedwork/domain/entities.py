import dacite

from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID

from pydantic import BaseModel

from seedwork.domain.events import DomainEvent
from seedwork.domain.mixins import BusinessRuleValidationMixin


@dataclass(kw_only=True)
class Entity:
    id: UUID

    def __post_init__(self) -> None:
        if not hasattr(self, "awaitable_attrs"):
            self.awaitable_attrs = AwaitableAttrs(entity=self)

    @classmethod
    def model_from(cls, model: BaseModel) -> Self:
        return dacite.from_dict(data_class=cls, data=model.model_dump())

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return dacite.from_dict(data_class=cls, data=data)

    def update(self, **kw) -> Any:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)


@dataclass(kw_only=True)
class LocalEntity(Entity):
    """Entity inside an aggregate."""


@dataclass(kw_only=True)
class AggregateRoot(BusinessRuleValidationMixin, Entity):
    """Consists of 1+ entities. Spans transaction boundaries."""

    def __post_init__(self) -> None:
        self.events: list[DomainEvent] = []

    def add_domain_event(self, event: DomainEvent) -> None:
        self.events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = self.events
        self.events = []  # noqa
        return events


class AwaitableAttrs:
    __slots__ = "_getter"

    def __init__(
        self, *, entity: Any = None, awaitable_attrs: Any = None
    ) -> None:
        assert (
            entity or awaitable_attrs
        ), "Either entity or awaitable_attrs must be provided"
        assert not (
            entity and awaitable_attrs
        ), "Only one of entity or awaitable_attrs can be provided"

        def attrs_getter(key: str):
            return getattr(awaitable_attrs, key)

        async def entity_getter(key: str):
            return getattr(entity, key)

        self._getter = attrs_getter if awaitable_attrs else entity_getter

    def __getattr__(self, key: str) -> Any:
        if key.startswith("_"):
            return object.__getattribute__(self, key)
        return self._getter(key)
