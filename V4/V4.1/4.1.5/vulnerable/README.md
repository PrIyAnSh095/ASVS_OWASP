# ASVS 4.1.5 Vulnerable Lab

## Overview

This vulnerable lab accepts requests without validating `X-Signature` properly. Missing, invalid, or tampered signatures are not enforced.

## Dependencies

- Flask

## Running vulnerable lab

```bash
cd V4/4.1.5/vulnerable
docker compose build
docker compose up
```

Open `http://localhost:5001` and test unsigned or tampered requests to observe insecure behavior.
