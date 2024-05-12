import importlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any as Json, cast, Any, Protocol
from uuid import UUID

from seedwork.application.application import Application
from seedwork.application.events import IntegrationEvent


@dataclass(kw_only=True)
class OutboxMessage:
    id: UUID
    occurred_on: datetime
    type: str
    data: Json
    processed_on: Optional[datetime] = None


class IMessageOutput(Protocol):
    async def publish(self, event: IntegrationEvent) -> None:
        ...

    async def get_unpublished(self) -> list[OutboxMessage]:
        ...

    async def mark_as_published(self, message: OutboxMessage) -> None:
        ...


class EventWorker:
    def __init__(
        self,
        app: Application,
        message_output: type[IMessageOutput],
    ) -> None:
        self._message_input = cast(Any, message_output)
        self._app = app

    @staticmethod
    def _get_cls_for(message_type: str) -> type:
        class_name = message_type.split(".")[-1]
        without_class_name = message_type.split(".")[:-1]
        module_name = ".".join(without_class_name)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)  # type: ignore

    async def process_outbox_message(self) -> None:
        async with self._app.transaction_context() as ctx:
            message_input = self._message_input(ctx["db_session"])
            messages = await message_input.get_unpublished()  # at least one
            for message in messages:
                event_cls = self._get_cls_for(message.type)
                event = event_cls(**json.loads(message.data))
                await ctx.publish_async(event)  # TODO: my own publish_async
                await message_input.mark_as_published(message)
