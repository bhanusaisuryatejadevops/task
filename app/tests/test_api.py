import json
from app import app

def test_sentiment_positive():
    client = app.test_client()
    r = client.post("/sentiment", json={"text":"I am happy"})
    assert r.status_code == 200
    body = r.get_json()
    assert body["sentiment"] in ["positive","neutral","negative"]
    assert "score" in body

def test_bad_request():
    client = app.test_client()
    r = client.post("/sentiment", data="{}",
                    headers={"Content-Type":"application/json"})
    assert r.status_code == 400
