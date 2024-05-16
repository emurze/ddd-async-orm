from typing import Coroutine

from seedwork.domain.events import DomainEvent


class FakeEventPublisher:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def __call__(self, event: DomainEvent) -> Coroutine:
        self.events.append(event)

        async def get_coroutine():
            return

        return get_coroutine()

    def contains(self, event: str | type[DomainEvent]) -> bool:
        return any(
            [
                type(ev).__name__ == event
                or isinstance(ev, event)  # type: ignore
                for ev in self.events
            ]
        )
