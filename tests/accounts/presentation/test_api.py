import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.e2e
async def test_can_create_account(ac: AsyncClient) -> None:
    response = await ac.post("/accounts/", json={"name": "Vlados"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Vlados"
