FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && python - <<'PY'
from textblob import download_corpora
try:
    download_corpora.download_all()
except Exception:
    pass
PY

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
