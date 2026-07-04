FROM python:3.12-slim

LABEL maintainer="ASVS-Labs"
LABEL description="ASVS 4.2.4 - Vulnerable: No CRLF Header Validation"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

# Use Hypercorn to serve the Flask app - note that even here, the HTTP/2
# framing layer prevents raw CRLF injection. The vulnerability is demonstrated
# at the application validation layer (missing input sanitization logic).
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:5001", "--workers", "1"]
