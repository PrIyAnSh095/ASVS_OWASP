# ASVS 4.1.2 Vulnerable Lab

## Overview

This vulnerable implementation fails ASVS control 4.1.2 by automatically redirecting both browser pages and API endpoints from HTTP to HTTPS. API requests may transmit sensitive data before the redirect occurs.

## Learning objectives

- Identify why API redirects are dangerous.
- Compare browser redirect behavior with harmful API redirects.
- Observe how `POST /api/login` can be redirected before secure transport is established.
- Use Docker Compose to run the vulnerable application on port `5001`.

## ASVS requirement

Control 4.1.2 requires that only user-facing endpoints automatically redirect from HTTP to HTTPS. Transparent redirects must not be applied to API or non-browser endpoints.

## Folder layout

- `app.py` — Flask application demonstrating insecure redirect behavior.
- `Dockerfile` — builds the vulnerable application container.
- `docker-compose.yml` — runs the vulnerable application on port `5001`.
- `requirements.txt` — Python dependencies.
- `.env` — runtime environment comments.

## Docker setup

Build the vulnerable container:

```bash
docker compose build
```

Start the vulnerable application:

```bash
docker compose up
```

The vulnerable service listens on `http://localhost:5001`.

## Running the vulnerable version

Use these endpoints:

- `http://localhost:5001/`
- `http://localhost:5001/api/login`
- `http://localhost:5001/api/profile`
- `http://localhost:5001/api/data`

## Browser testing

1. Open developer tools and enable the Network tab.
2. Visit `http://localhost:5001/`.
3. Confirm the response redirects to `https://localhost:5001/`.
4. Visit `http://localhost:5001/api/profile`.
5. Confirm the request also redirects to HTTPS.

## curl testing

Examples:

```bash
curl -i http://localhost:5001/
```

```bash
curl -i -X POST http://localhost:5001/api/login -H 'Content-Type: application/json' -d '{"username":"student"}'
```

```bash
curl -i http://localhost:5001/api/profile
```

```bash
curl -i http://localhost:5001/api/data
```

## Burp testing

1. Configure Burp to proxy HTTP traffic.
2. Capture requests to `http://localhost:5001/` and `/api/*`.
3. Confirm all HTTP requests return redirects to HTTPS.
4. Observe `307` redirects for API endpoints preserving the request method.

## Expected behavior

- Browser pages should redirect from HTTP to HTTPS.
- API endpoints should also redirect, which is insecure for this lab.
- Sensitive API requests should not be silently upgraded.

## Learning outcomes

Students will understand why transparent API redirects are unsafe and how this vulnerable behavior fails ASVS 4.1.2.
