import pytest
from httpx import AsyncClient


@pytest.mark.e2e
async def test_can_create_account(ac: AsyncClient) -> None:
    response = await ac.post("/accounts/", json={"name": "Vlados"})
    assert response.json()["name"] == "Vlados"
