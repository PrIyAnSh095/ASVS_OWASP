# ASVS 4.1.5 Message Signing Lab

## Overview

This lab demonstrates ASVS 4.1.5 by comparing a secure message signing implementation with a vulnerable one. The secure application verifies HMAC-SHA256 signatures on sensitive requests. The vulnerable application accepts requests without effective signature validation.

## Learning Objectives

- Learn how HMAC-SHA256 signature verification works.
- Understand why per-message signing provides message integrity beyond TLS.
- Observe rejection of missing, invalid, or tampered signatures.
- Compare secure and vulnerable behavior using Browser, Burp, and curl.

## ASVS Requirement

Control 4.1.5 requires per-message digital signatures for highly sensitive requests or those traversing multiple systems.

## Project Structure

- `secure/` — secure Flask implementation with Docker support.
- `vulnerable/` — vulnerable Flask implementation with Docker support.
- `templates/` — shared templates for the frontend.
- `static/` — shared CSS and JavaScript.
- `docs/` — educational documentation.
- `tests/` — example curl and Burp test cases.

## Docker Setup

Secure lab:

```bash
cd V4/4.1.5/secure
docker compose build
docker compose up
```

Vulnerable lab:

```bash
cd V4/4.1.5/vulnerable
docker compose build
docker compose up
```

## Running Secure

Open `http://localhost:5000` and use the dashboard to generate a signature, then send requests.

## Running Vulnerable

Open `http://localhost:5001` and send requests. The vulnerable app will accept missing or invalid signatures.

## Browser Testing

- Generate a signature.
- Send a valid signed request.
- Tamper the payload and resend.
- Observe the secure lab rejects the tampered request.

## Burp Testing

- Capture a signed request.
- Modify the body or remove the signature.
- Re-send and compare secure vs vulnerable behavior.

## curl Testing

Use the example commands in `docs/curl.md`.

## PASS Behavior

- Signature required.
- Signature verified.
- Tampered messages rejected.
- Invalid signatures rejected.
- Missing signatures rejected.

## FAIL Behavior

- Missing signatures accepted.
- Invalid signatures accepted.
- Tampered requests processed.
- Request integrity not verified.

## Learning Outcomes

Students should understand how HMAC protects request integrity, why per-message signatures are needed in addition to TLS, and how to test ASVS 4.1.5 compliance.
