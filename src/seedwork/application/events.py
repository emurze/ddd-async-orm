from dataclasses import field
from typing import Any, Optional

from seedwork.application.dtos import Result
from seedwork.domain.errors import Error
from seedwork.domain.events import DomainEvent


class IntegrationEvent(DomainEvent):
    """
    Integration events are used to communicate between modules/system via inbox-outbox pattern.
    They are created in a domain event handler and then saved in an outbox for further delivery.
    As a result, integration events are handled asynchronously.
    """


class EventResult(Result):
    payload: Any = None
    events: list[IntegrationEvent | DomainEvent] = field(default_factory=list)
    error: Optional[Error] = None
