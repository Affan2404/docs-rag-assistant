from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_query_valid_question():
    response = client.post("/query", json={"question": "How do I create an hourly automation rule?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)

def test_query_missing_question_field():
    response = client.post("/query", json={})
    assert response.status_code == 422