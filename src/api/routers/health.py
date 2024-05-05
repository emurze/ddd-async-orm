import uuid
from pprint import pprint

from fastapi import APIRouter, Depends
from lato import Application

from api.deps import get_application
from modules.accounts.application.query import GetAccountQuery

health_router = APIRouter()


@health_router.get("/health")
async def health(app: Application = Depends(get_application)) -> dict:
    print(f"{app=}")
    res = await app.execute_async(GetAccountQuery(id=uuid.uuid4()))
    print(f"{res=}")
    # pprint(vars(app))
    # pprint(dir(app))
    return {"status": "ok"}
