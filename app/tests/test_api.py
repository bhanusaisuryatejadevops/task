# tests/test_api.py
import pytest
from app.app import app  # import the Flask app instance

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_sentiment_positive(client):
    response = client.post("/sentiment", json={"text": "I am very happy"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["sentiment"] == "positive"
    assert "score" in data

def test_sentiment_negative(client):
    response = client.post("/sentiment", json={"text": "I am sad"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["sentiment"] == "negative"
    assert "score" in data

def test_sentiment_neutral(client):
    response = client.post("/sentiment", json={"text": "It is a table"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["sentiment"] == "neutral"
    assert "score" in data

def test_sentiment_missing_text(client):
    response = client.post("/sentiment", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
