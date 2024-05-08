from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends

from api.deps import get_application
from api.schemas.accounts import AccountJsonResponse, AccountJsonRequest
from modules.accounts.application.command import CreateAccountCommand
from modules.accounts.application.query import GetAccountQuery
from seedwork.application.application import Application

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get(
    "/{account_id}",
    response_model=AccountJsonResponse,
    status_code=HTTPStatus.OK,
)
async def get_account(
    account_id: UUID,
    app: Application = Depends(get_application),
):
    res = await app.execute_async(GetAccountQuery(id=account_id))
    return res.payload


@router.post(
    "/",
    response_model=AccountJsonResponse,
    status_code=HTTPStatus.CREATED,
)
async def create_account(
    request_body: AccountJsonRequest,
    app: Application = Depends(get_application),
):
    command = CreateAccountCommand.model_validate(request_body)
    await app.execute_async(command)
    res = await app.execute_async(GetAccountQuery(id=command.id))
    print(f"{res=}")
    return res.payload
