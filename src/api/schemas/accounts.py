from uuid import UUID

from seedwork.presentation.schemas import Schema


class AccountJsonResponse(Schema):
    id: UUID
    name: str


class AccountJsonRequest(Schema):
    name: str
