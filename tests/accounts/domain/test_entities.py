import pytest

from accounts.domain.entities import Account
from accounts.domain.value_objects import Address, AccountId
from seedwork.domain.services import next_id


@pytest.mark.unit
def test_account_can_change_name_successfully() -> None:
    # arrange
    account_id = AccountId(next_id())
    address = Address(country="France", city="Paris")
    account = Account(id=account_id, name="Account 1", address=address)

    # act
    res = account.change_name("Account 2")

    # assert
    assert res.is_ok(), "Account name should be changed successfully"
    assert account.name == "Account 2", "Account name should be updated"


@pytest.mark.unit
def test_account_cannot_change_name_when_no_address_provided() -> None:
    # arrange
    account_id = AccountId(next_id())
    account = Account(id=account_id, name="Account 1", address=None)

    # act
    res = account.change_name("Account 2")

    # assert
    assert res.is_err(), "Changing name should return an error when address is None"


@pytest.mark.unit
def test_account_can_get_name_card_successfully() -> None:
    # arrange
    account_id = AccountId(next_id())
    address = Address(country="France", city="Paris")
    account = Account(id=account_id, name="Account 1", address=address)

    # act
    name = account.get_name_card()

    # assert
    assert name.is_ok(), "Getting name card should be successful"
    assert name.ok_value == f"Account 1-{address}", (
        "Name card should be generated correctly"
    )
