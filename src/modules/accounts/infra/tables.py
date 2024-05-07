from sqlalchemy import Table, Column, UUID, String

from modules.accounts.domain.entities import Account
from seedwork.infra.database import base_registry

account_table = Table(
    "account",
    base_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("name", String, nullable=False),
)


def start_mappers() -> None:
    base_registry.map_imperatively(Account, account_table)
