from uuid import UUID

from modules.accounts.application import account_module
from seedwork.application.queries import Query


class GetAccountQuery(Query):
    id: UUID


@account_module.handler(GetAccountQuery)
async def get_account(query: GetAccountQuery) -> dict:
    print(f"GET ACCOUNT {query=}")
    return {"data": "New Account"}
