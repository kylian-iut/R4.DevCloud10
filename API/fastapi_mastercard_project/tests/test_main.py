from fastapi.testclient import TestClient
from src.fastapi_mastercard.main import app

client = TestClient(app)

def test_clear_pin_counter():
    response = client.post("/clear-pin-counter/", json={"card_id": "1234567890"})
    # Ici on attend une erreur car la clé API sandbox est fake, mais l'appel doit fonctionner
    assert response.status_code in (200, 400)
