from datetime import datetime

from sqlalchemy import (
    Table, UUID, Column, DateTime, String, JSON, null, select
)
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.application.events import IntegrationEvent
from seedwork.application.inbox_outbox import OutboxMessage
from seedwork.domain.services import next_id
from seedwork.infra.database import base_registry

outbox_message_table = Table(
    "outbox_messages",
    base_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("occurred_on", DateTime, nullable=False),
    Column("type", String, nullable=False),
    Column("data", JSON, nullable=False),
    Column("processed_on", DateTime)
)


def start_outbox_mappers() -> None:
    base_registry.map_imperatively(OutboxMessage, outbox_message_table)


class SqlAlchemyMessageOutbox:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def publish(self, event: IntegrationEvent) -> None:
        outbox_message = OutboxMessage(
            id=next_id(),
            occurred_on=datetime.utcnow(),
            type=f"{type(event).__module__}.{type(event).__name__}",
            data=event.model_dump_json(),
        )
        self._session.add(outbox_message)

    async def get_unpublished(self) -> list[OutboxMessage]:
        stmt = (
            select(OutboxMessage)
            .where(OutboxMessage.processed_on == null())
            .order_by(OutboxMessage.occurred_on)
            .limit(100)
        )
        res = await self._session.execute(stmt)
        return list(res.scalars())

    async def mark_as_published(self, message: OutboxMessage) -> None:
        await self._session.merge(
            OutboxMessage(
                id=message.id,
                occurred_on=message.occurred_on,
                type=message.type,
                data=message.data,
                processed_on=datetime.utcnow(),
            )
        )
