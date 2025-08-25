import json
from app import app  # this works if app/__init__.py exists

def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_sentiment_positive():
    client = app.test_client()
    resp = client.post("/sentiment", 
        data=json.dumps({"text": "I am very happy today"}),
        content_type="application/json"
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["sentiment"] == "positive"

def test_sentiment_negative():
    client = app.test_client()
    resp = client.post("/sentiment", 
        data=json.dumps({"text": "I am very tired today"}),
        content_type="application/json"
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["sentiment"] == "negative"
