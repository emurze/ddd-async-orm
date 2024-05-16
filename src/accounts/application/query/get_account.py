from dataclasses import asdict
from uuid import UUID

from accounts.application import accounts_module
from accounts.domain.repositories import IAccountRepository
from seedwork.application.queries import Query
from seedwork.domain.errors import Error


class GetAccountQuery(Query):
    id: UUID


@accounts_module.handler(GetAccountQuery)
async def get_account(
    query: GetAccountQuery,
    account_repository: IAccountRepository,
) -> dict | Error:
    account = await account_repository.get_by_id(query.id)

    if not account:
        return Error.not_found()

    return asdict(account)
