# ASVS 4.1.2 Secure Lab

## Overview

This secure implementation demonstrates correct behavior for ASVS control 4.1.2. Only user-facing browser pages automatically redirect from HTTP to HTTPS. API endpoints reject HTTP and require the client to retry using HTTPS.

## Learning objectives

- Understand why browser redirects are acceptable for user-facing pages.
- Learn why API endpoints must not transparently redirect.
- Verify that only `/` redirects and `/api/*` rejects HTTP.
- Use Docker Compose to run the lab independently.
- Inspect the behavior with browser tools, curl, and Burp.

## ASVS requirement

Control 4.1.2 requires that only user-facing endpoints automatically redirect from HTTP to HTTPS. Services and API endpoints must not implement transparent redirects because sensitive information can be sent before the redirect occurs.

## Folder layout

- `app.py` — Flask application demonstrating secure redirect behavior.
- `Dockerfile` — builds the secure application container.
- `docker-compose.yml` — runs the secure application on port `5000`.
- `requirements.txt` — Python dependencies.
- `.env` — runtime environment comments.

## Docker setup

Build the secure container:

```bash
docker compose build
```

Start the secure application:

```bash
docker compose up
```

The secure service listens on `http://localhost:5000`.

## Running the secure version

Use these endpoints:

- `http://localhost:5000/`
- `http://localhost:5000/api/login`
- `http://localhost:5000/api/profile`
- `http://localhost:5000/api/data`

## Browser testing

1. Open developer tools and enable the Network tab.
2. Visit `http://localhost:5000/`.
3. Confirm the response is a redirect to `https://localhost:5000/`.
4. Visit `http://localhost:5000/api/profile`.
5. Confirm the response is `403 Forbidden` and no redirect occurs.

## curl testing

Examples:

```bash
curl -i http://localhost:5000/
```

```bash
curl -i -X POST http://localhost:5000/api/login -H 'Content-Type: application/json' -d '{"username":"student"}'
```

```bash
curl -i http://localhost:5000/api/profile
```

```bash
curl -i http://localhost:5000/api/data
```

## Burp testing

1. Configure Burp to proxy HTTP traffic.
2. Capture requests to `http://localhost:5000/` and `/api/*`.
3. Confirm the browser page redirects to HTTPS.
4. Confirm API requests return `403` without a Location header.

## Expected behavior

- `/` should redirect from HTTP to HTTPS.
- `/api/login`, `/api/profile`, and `/api/data` should reject HTTP.
- API endpoints should never silently upgrade HTTP to HTTPS.

## Learning outcomes

Students will understand why browser-only redirect rules are needed, why APIs must reject HTTP, and how to compare secure behavior against the vulnerable implementation in the sibling lab.
