from uuid import UUID

from seedwork.presentation.schemas import Schema


class AddressJson(Schema):
    city: str | None
    country: str | None


class AccountJsonResponse(Schema):
    id: UUID
    name: str
    address: AddressJson | None = None


class AccountJsonRequest(Schema):
    name: str
    address: AddressJson | None = None
