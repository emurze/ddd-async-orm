from uuid import UUID

from seedwork.application.events import IntegrationEvent


class AccountCreatedEvent(IntegrationEvent):
    id: UUID
