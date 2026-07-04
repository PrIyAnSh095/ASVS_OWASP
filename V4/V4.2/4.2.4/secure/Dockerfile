FROM python:3.12-slim

LABEL maintainer="ASVS-Labs"
LABEL description="ASVS 4.2.4 - Secure: CRLF Header Injection Prevention"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Use Hypercorn (ASGI/HTTP2 capable) to serve the Flask app over HTTP/2
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "1"]
