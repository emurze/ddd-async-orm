from seedwork.domain.events import DomainEvent


class FakeEventPublisher:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def __call__(self, event: DomainEvent) -> None:
        self.events.append(event)

    def contains(self, event: str | type[DomainEvent]) -> bool:
        return any([
            type(ev).__name__ == event or isinstance(ev, event)  # type: ignore
            for ev in self.events
        ])
