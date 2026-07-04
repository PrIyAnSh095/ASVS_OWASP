# ASVS 4.1.3 Secure Lab

## Overview

This secure lab simulates a backend behind a trusted reverse proxy. It ignores client-supplied proxy headers such as `X-Forwarded-For` and `X-User-ID`, using only internally trusted values.

## Learning objectives

- Understand why headers like `X-Forwarded-For` should only be trusted from infrastructure.
- Verify that spoofed client headers do not affect identity, host, or protocol detection.
- Use the frontend to supply spoofed values and observe no change.

## ASVS requirement

Control 4.1.3 requires that HTTP headers set by intermediary layers cannot be overridden by end-users.

## Running secure lab

Build and run:

```bash
docker compose build
``` 

```bash
docker compose up
```

Visit `http://localhost:5000/` and use the form to submit spoofed header values. The secure app always displays the trusted internal values.
