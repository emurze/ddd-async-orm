from lato import Event
from pydantic_settings import SettingsConfigDict

generic_model_config = SettingsConfigDict(
    frozen=True,
    from_attributes=True,
    arbitrary_types_allowed=True,
    extra="allow",
)


class DomainEvent(Event):
    """
    Domain events are used to communicate between aggregates within
    a single transaction boundary via in-memory queue.
    Domain events are synchronous in nature.
    """

    model_config = generic_model_config

    def __next__(self):
        yield self
