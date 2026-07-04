# ASVS 4.2.2 Secure Lab

This secure lab implements correct HTTP response framing by calculating `Content-Length` from the actual response body bytes.

## Run

```powershell
cd V4\V4.2\4.2.2\secure
docker compose build
docker compose up
```

Visit `http://localhost:5000`.

## Behavior

- The app always computes `Content-Length` after serializing the body.
- The declared header value matches the actual byte count.
- The response is RFC 9112 compliant.
