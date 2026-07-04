# ASVS 4.1.3 Vulnerable Lab

## Overview

This vulnerable lab reads trusted values directly from client-supplied proxy headers. Spoofed headers such as `X-Forwarded-For` and `X-User-ID` change the detected identity and protocol.

## Learning objectives

- Observe how client-supplied proxy headers can be abused.
- Compare secure and vulnerable handling of the same spoofed headers.
- Understand why infrastructure must inject these headers, not clients.

## Running vulnerable lab

Build and run:

```bash
docker compose build
``` 

```bash
docker compose up
```

Visit `http://localhost:5001/` and submit spoofed header values. The vulnerable app displays the spoofed values.
