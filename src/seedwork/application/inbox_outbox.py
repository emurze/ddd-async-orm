import importlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any as Json, Any
from uuid import UUID

from seedwork.application.application import Application


@dataclass(kw_only=True)
class OutboxMessage:
    id: UUID
    occurred_on: datetime
    type: str
    data: Json
    processed_on: Optional[datetime] = None


@dataclass(frozen=True, slots=True)
class EventProducer:
    message_output: Any
    app: Application

    @staticmethod
    def _get_cls_for(message_type: str) -> type:
        class_name = message_type.split(".")[-1]
        without_class_name = message_type.split(".")[:-1]
        module_name = ".".join(without_class_name)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)  # type: ignore

    async def process_outbox_message(self) -> None:
        async with self.app.transaction_context() as ctx:
            message_output = self.message_output(ctx["db_session"])
            messages = await message_output.get_unpublished()  # at least one
            for message in messages:
                event_cls = self._get_cls_for(message.type)
                event = event_cls(**json.loads(message.data))

                # publish_to_rabbitmq()

                await message_output.mark_as_published(message)
