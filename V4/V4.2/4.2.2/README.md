# ASVS V4.2.2 HTTP Response Content-Length Lab

## Overview

This lab demonstrates ASVS 4.2.2 by comparing secure HTTP response generation with correct `Content-Length` handling against a vulnerable implementation that intentionally misreports `Content-Length`.

The secure lab always calculates the actual byte length of the serialized response body and sets the `Content-Length` header accordingly. The vulnerable lab sets an incorrect length to demonstrate response framing failures.

## Project Structure

- `secure/` — secure Flask lab with correct `Content-Length` values.
- `vulnerable/` — vulnerable Flask lab with mismatched `Content-Length` values.
- `templates/` — shared frontend templates.
- `static/` — shared CSS and JavaScript.
- `docs/` — theory, attacks, testing guides, and expected results.
- `tests/` — example curl commands, Burp requests, and sample payloads.

## How to run

### Secure lab

```powershell
cd V4\V4.2\4.2.2\secure
docker compose build
docker compose up
```

Open `http://localhost:5000`.

### Vulnerable lab

```powershell
cd V4\V4.2\4.2.2\vulnerable
docker compose build
docker compose up
```

Open `http://localhost:5001`.

## Validation

Secure lab: declared and actual lengths always match.
Vulnerable lab: declared length intentionally differs from actual length.
