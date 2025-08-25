from flask import Flask, request, jsonify
from textblob import TextBlob
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQ_COUNT = Counter(
    "sentiment_requests_total",
    "Total number of /sentiment requests",
    ["status"]
)
REQ_LATENCY = Histogram(
    "sentiment_request_latency_seconds",
    "Latency for /sentiment requests in seconds"
)

@app.route("/", methods=["GET"])
def index():
    return (
        "<h2>🚀 Welcome to the AI Sentiment Analysis API</h2>"
        "<p>Use <b>POST /sentiment</b> with JSON like "
        "<code>{\"text\": \"I am happy\"}</code> "
        "to analyze sentiment.</p>"
    )

@app.route("/sentiment", methods=["POST"])
def sentiment():
    start = time.time()
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "").strip()
        if not text:
            REQ_COUNT.labels(status="400").inc()
            return jsonify({"error": "Provide JSON {\"text\": \"I am happy\"}"}), 400

        blob = TextBlob(text)
        polarity = float(blob.sentiment.polarity)
        subjectivity = float(blob.sentiment.subjectivity)
        label = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"

        resp = {
            "text": text,
            "sentiment": label,
            "score": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        }
        REQ_COUNT.labels(status="200").inc()
        return jsonify(resp), 200
    except Exception:
        REQ_COUNT.labels(status="500").inc()
        raise
    finally:
        REQ_LATENCY.observe(time.time() - start)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
