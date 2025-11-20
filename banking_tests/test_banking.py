"""Test File for Banking Service"""

import pytest

def bank_account_details_payload(id=1, name="John", email="John@Example.com", pin=1225, card="1000000000000000", balance=2):
    return {"id": id, "name": name, "email": email, "pin": pin, "card": card, "balance": balance}

def bank_account_details_payload_post(name="John", email="John@Example.com", pin=1225, card="1000000000000000", balance=2):
    return {"name": name, "email": email, "pin": pin, "card": card, "balance": balance}

def test_create_bank_account_ok(client):
    """tests if you can successfully create a user"""
    result = client.post("/api/banking", json=bank_account_details_payload_post())
    assert result.status_code == 201
    data = result.json()
    assert data["name"] == "John"

def test_get_banking_details_404(client):
    """tests 404 is thrown when a user does not exist when trying to get them"""
    result = client.get("/api/banking/999")
    assert result.status_code == 404

def test_delete_then_404(client):
    """tests 404 is throw when trying to delete a user who does not exist"""
    client.post("/api/banking", json=bank_account_details_payload_post())
    result1 = client.delete("/api/banking/1")
    assert result1.status_code == 204
    result2 = client.delete("/api/banking/1")
    assert result2.status_code == 404

def test_edit_account_details_ok(client):
    """tests you can edit an existing user"""
    client.post("/api/banking", json=bank_account_details_payload_post())
    result1 = client.put("/api/banking/1", json=bank_account_details_payload(id=1, name="Jill"))
    assert result1.status_code == 200
    data = result1.json()
    assert data["name"] == "Jill"

def test_edit_account_details_404(client):
    """tests you can't edit a user that does not exist"""
    result = client.put("/api/banking/2", json=bank_account_details_payload(name="Jill"))
    assert result.status_code == 404

@pytest.mark.parametrize("bad_email", ["BADEMAIL123", "@123.ie", "BAD@", "badmail"])
def test_bad_email_422(client, bad_email):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/banking", json=bank_account_details_payload_post(email=bad_email))
    assert result.status_code == 422 # pydantic validation error

@pytest.mark.parametrize("bad_pin", ["BADPIN123", 12345,-2, 999, "@!?"])
def test_bad_pin_422(client, bad_pin):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/banking", json=bank_account_details_payload_post(pin=bad_pin))
    assert result.status_code == 422 # pydantic validation error

@pytest.mark.parametrize("bad_card", ["BADEMAIL123", "@123.ie", "BAD@", "badmail",-2, 0,1000000000000000])
def test_bad_card_422(client, bad_card):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/banking", json=bank_account_details_payload_post(card=bad_card))
    assert result.status_code == 422 # pydantic validation error

@pytest.mark.parametrize("bad_balance", ["1BAL", -2, "balance"])
def test_bad_balance_422(client, bad_balance):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/banking", json=bank_account_details_payload_post(balance=bad_balance))
    assert result.status_code == 422 # pydantic validation error