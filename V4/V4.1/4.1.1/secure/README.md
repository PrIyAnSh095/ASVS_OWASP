# ASVS 4.1.1 Secure Lab

## Overview

This folder contains the secure implementation for ASVS control 4.1.1. The application demonstrates correct HTTP Content-Type handling for every response with a message body.

## Learning objectives

- Understand the purpose of the `Content-Type` header.
- Verify that response bodies carry the correct MIME type.
- Confirm `charset=UTF-8` is present when text media is served.
- Use Docker to run an isolated Flask lab.
- Inspect HTTP headers with browser developer tools, curl, and Burp.

## ASVS requirement

Control 4.1.1 requires every HTTP response with a message body to include a `Content-Type` header that matches the actual content and includes the `charset` parameter.

## Folder layout

- `app.py` — Flask application serving secure responses.
- `Dockerfile` — container configuration for the secure lab.
- `docker-compose.yml` — service definition for local testing.
- `requirements.txt` — Python dependencies.
- `.env` — explanatory environment file (not required for runtime).

## Docker setup

Build the secure container:

```bash
docker compose build
```

Start the secure service:

```bash
docker compose up
```

The service listens on `http://localhost:5000`.

## Running the secure version

Open a browser and visit:

- `http://localhost:5000/`
- `http://localhost:5000/json`
- `http://localhost:5000/html`
- `http://localhost:5000/xml`
- `http://localhost:5000/text`

## Browser verification

1. Open developer tools.
2. Navigate to the Network tab.
3. Reload the endpoint.
4. Select the request and inspect the Response Headers.
5. Confirm `Content-Type` matches the payload and contains `charset=UTF-8`.

## curl verification

Use these commands:

```bash
curl -i http://localhost:5000/json
curl -i http://localhost:5000/html
curl -i http://localhost:5000/xml
curl -i http://localhost:5000/text
```

Expected results:

- `Content-Type: application/json; charset=UTF-8`
- `Content-Type: text/html; charset=UTF-8`
- `Content-Type: application/xml; charset=UTF-8`
- `Content-Type: text/plain; charset=UTF-8`

## Burp verification

1. Configure Burp proxy.
2. Send traffic from your browser or curl through Burp.
3. Capture the request and forward it.
4. Send the request to Repeater.
5. Review the response headers and validate `Content-Type` and `charset`.

## Learning outcomes

Students should be able to explain why correct `Content-Type` headers are critical, identify safe response handling in Flask, and compare the secure implementation against the vulnerable version located in `../vulnerable`.
