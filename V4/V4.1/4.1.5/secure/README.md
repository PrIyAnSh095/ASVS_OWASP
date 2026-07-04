# ASVS 4.1.5 Secure Lab

## Overview

This secure lab demonstrates HMAC-SHA256 request signing. The application rejects missing, invalid, or tampered `X-Signature` headers.

## Dependencies

- Flask

## Running secure lab

```bash
cd V4/4.1.5/secure
docker compose build
docker compose up
```

Open `http://localhost:5000` to use the frontend and test signed requests.
