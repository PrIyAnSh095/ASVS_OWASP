# ASVS 4.1.1 Vulnerable Lab

## Overview

This folder contains the intentionally vulnerable implementation for ASVS control 4.1.1. The application functions, but it fails the Content-Type requirement by returning incorrect or incomplete MIME headers.

## Learning objectives

- Compare secure and vulnerable Content-Type handling.
- Identify wrong MIME type declarations.
- Detect missing `charset=UTF-8` values.
- Inspect HTTP responses with browser tools, curl, and Burp.

## ASVS requirement

Control 4.1.1 requires every HTTP response with a message body to include a `Content-Type` header that accurately describes the payload and includes `charset=UTF-8` for text-based content.

## Folder layout

- `app.py` — Flask application demonstrating invalid Content-Type headers.
- `Dockerfile` — container configuration for the vulnerable lab.
- `docker-compose.yml` — service definition for local testing.
- `requirements.txt` — Python dependencies.
- `.env` — explanatory file not required for runtime.

## Docker setup

Build the vulnerable container:

```bash
cd vulnerable
docker compose build
```

Start the vulnerable service:

```bash
docker compose up
```

The service listens on `http://localhost:5001`.

## Running the vulnerable version

Open a browser and visit:

- `http://localhost:5001/`
- `http://localhost:5001/json`
- `http://localhost:5001/html`
- `http://localhost:5001/xml`
- `http://localhost:5001/text`

## Browser verification

Inspect the response headers and confirm the vulnerable version deliberately returns incorrect MIME types or missing charset values.

## curl verification

Use these commands:

```bash
curl -i http://localhost:5001/json
curl -i http://localhost:5001/html
curl -i http://localhost:5001/xml
curl -i http://localhost:5001/text
```

The vulnerable app should show incorrect `Content-Type` headers while still returning valid bodies.

## Burp verification

Use Burp Proxy and Repeater to compare the vulnerable service against the secure implementation on port `5000`.

## Learning outcomes

Students should be able to explain why these header mismatches are unsafe, and show how even a functioning application can fail ASVS 4.1.1.
