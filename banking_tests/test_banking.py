"""Test File for Banking Service"""

import pytest

def card_payload(user_id=1, creditCardNumber="1111222233334444",nameOnCard="Ionaton",expMonth=2, expYear=2028,cvc=111):
    return{"user_id": user_id, "creditCardNumber":creditCardNumber, "nameOnCard":nameOnCard, "expMonth":expMonth, "expYear": expYear,"cvc":cvc}

def test_create_bank_card_ok(mock_rabbitmq, client):
    """tests if you can successfully create a card"""
    result = client.post("/api/banking", json=card_payload())
    assert result.status_code == 201
    mock_rabbitmq.assert_called()

def test_get_bank_card_404(client):
    """tests 404 is thrown when a card does not exist when trying to get them"""
    result = client.get("/api/banking/999")
    assert result.status_code == 404



def test_delete_card_then_404(mock_rabbitmq, client):
    """tests 404 is throw when trying to delete a card which does not exist"""
    client.post("/api/banking", json=card_payload())
    result1 = client.delete("/api/banking/1")
    assert result1.status_code == 204
    result2 = client.delete("/api/banking/1")
    assert result2.status_code == 404
    mock_rabbitmq.assert_called()

@pytest.mark.parametrize("bad_creditCardNumber", [12345677, "1234536", "BadString12"])
def test_bad_creditCardNumber_422(client, bad_creditCardNumber):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/banking", json=card_payload(creditCardNumber=bad_creditCardNumber))
    assert result.status_code == 422 # pydantic validation error

def test_get_all_bank_cards(mock_rabbitmq, client):
    """tests getting all bank cards"""
    client.post("/api/banking", json=card_payload())
    result = client.get("/api/banking")
    assert result.status_code == 200
    assert len(result.json()) == 1
    mock_rabbitmq.assert_called()

def test_get_bank_card_ok(mock_rabbitmq, client):
    """tests getting a specific bank card"""
    payload = card_payload(creditCardNumber="5555666677778888")
    client.post("/api/banking", json=payload)
    result = client.get("/api/banking/1")
    assert result.status_code == 200
    mock_rabbitmq.assert_called()

def test_patch_card_ok(mock_rabbitmq, client):
    """tests partial update of bank card"""
    client.post("/api/banking", json=card_payload())
    result = client.patch("/api/banking/1", json={"creditCardNumber": "5555666677778888"})
    assert result.status_code == 200
    assert result.json()["creditCardNumber"] == "5555666677778888"
    mock_rabbitmq.assert_called()

def test_patch_card_404(mock_rabbitmq, client):
    """tests patch on non-existent card"""
    result = client.patch("/api/banking/999", json={"creditCardNumber": "5555666677778888"})
    assert result.status_code == 404
    mock_rabbitmq.assert_called()
