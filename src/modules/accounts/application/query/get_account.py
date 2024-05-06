from uuid import UUID

from modules.accounts.application import accounts_module
from seedwork.application.queries import Query


class GetAccountQuery(Query):
    id: UUID


@accounts_module.handler(GetAccountQuery)
async def get_account(query: GetAccountQuery) -> dict:
    return {"id": query.id, "name": "Vlados"}
