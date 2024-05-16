from sqlalchemy import Table, Column, UUID, String
from sqlalchemy.orm import composite

from accounts.domain.entities import Account
from accounts.domain.value_objects import Address
from seedwork.infra.database import base_registry

account_table = Table(
    "account",
    base_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("name", String, nullable=False),
    Column("country", String, nullable=True),
    Column("city", String, nullable=True),
)


def start_mappers() -> None:
    base_registry.map_imperatively(
        Account,
        account_table,
        properties={
            "address": composite(
                Address, account_table.c.country, account_table.c.city
            ),
        }
    )
