# ASVS 4.2.2 Vulnerable Lab

This vulnerable lab misreports `Content-Length` to demonstrate HTTP response framing failures and protocol desynchronization.

## Run

```powershell
cd V4\V4.2\4.2.2\vulnerable
docker compose build
docker compose up
```

Visit `http://localhost:5001`.

## Behavior

- The app intentionally sets an incorrect `Content-Length` header.
- The body is still delivered, but the declared length does not match the actual bytes.
- This is a protocol violation and can lead to proxy desynchronization.
