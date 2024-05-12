from modules.accounts.application.event import AccountCreatedEvent
from modules.notifications.application import notifications_module


@notifications_module.handler(AccountCreatedEvent)
async def print_hello(event: AccountCreatedEvent) -> None:
    """Idempotent event handler"""
    print(f"HELLO WORLD {event=}")
