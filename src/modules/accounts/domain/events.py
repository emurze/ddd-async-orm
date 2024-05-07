from uuid import UUID

from seedwork.domain.events import DomainEvent


class AccountCreatedEvent(DomainEvent):
    id: UUID
