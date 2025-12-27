"""Test File for Banking Service"""

import pytest

def card_payload(user_id=1, card_number="1111222233334444",name_on_card="Ionaton",month_of_expiry=2, year_of_expiry=2028,cvc=111):
    return{"user_id": user_id, "card_number":card_number, "name_on_card":name_on_card, "month_of_expiry":month_of_expiry, "year_of_expiry": year_of_expiry,"cvc":cvc}

def test_create_bank_account_ok(mock_rabbitmq, client):
    """tests if you can successfully create a user"""
    result = client.post("/api/banking", json=card_payload())
    assert result.status_code == 201
    mock_rabbitmq.assert_called()

def test_get_banking_details_404(client):
    """tests 404 is thrown when a user does not exist when trying to get them"""
    result = client.get("/api/banking/999")
    assert result.status_code == 404

def test_delete_then_404(mock_rabbitmq, client):
    """tests 404 is throw when trying to delete a user who does not exist"""
    client.post("/api/banking", json=card_payload())
    result1 = client.delete("/api/banking/1")
    assert result1.status_code == 204
    result2 = client.delete("/api/banking/1")
    assert result2.status_code == 404
    mock_rabbitmq.assert_called()

@pytest.mark.parametrize("bad_card_number", [12345677, "1234536", "BadString12"])
def test_bad_card_number_422(client, bad_card_number):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/banking", json=card_payload(card_number=bad_card_number))
    assert result.status_code == 422 # pydantic validation error

def test_get_all_bank_cards(mock_rabbitmq, client):
    """tests getting all bank accounts"""
    client.post("/api/banking", json=card_payload())
    result = client.get("/api/banking")
    assert result.status_code == 200
    assert len(result.json()) == 1
    mock_rabbitmq.assert_called()

def test_get_bank_card_ok(mock_rabbitmq, client):
    """tests getting a specific bank account"""
    payload = card_payload(card_number="5555666677778888")
    client.post("/api/banking", json=payload)
    result = client.get("/api/banking/1")
    assert result.status_code == 200
    assert result.json()["card_number"] == "5555666677778888"
    mock_rabbitmq.assert_called()

def test_patch_card_ok(mock_rabbitmq, client):
    """tests partial update of bank account"""
    client.post("/api/banking", json=card_payload())
    result = client.patch("/api/banking/1", json={"card_number": "5555666677778888"})
    assert result.status_code == 200
    assert result.json()["card_number"] == "5555666677778888"
    mock_rabbitmq.assert_called()

def test_patch_account_404(client):
    """tests patch on non-existent account"""
    result = client.patch("/api/banking/999", json={"card_number": "5555666677778888"})
    assert result.status_code == 404
