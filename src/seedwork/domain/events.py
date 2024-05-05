from lato import Event
from pydantic import ConfigDict


class DomainEvent(Event):
    """
    Domain events are used to communicate between aggregates within
    a single transaction boundary via in-memory queue.
    Domain events are synchronous in nature.
    """
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    def __next__(self):
        yield self
