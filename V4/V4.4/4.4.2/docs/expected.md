# Expected Behavior

## Secure Implementation
* The server maintains an explicit list of trusted Origins (e.g., the domains where the frontend is hosted).
* During the HTTP handshake, the server compares the incoming `Origin` header against the allowlist.
* Untrusted origins receive an HTTP 400 (Bad Request) or 403 (Forbidden).
* The WebSocket connection is never established.

## Vulnerable Implementation
* The server ignores the `Origin` header.
* It blindly upgrades the connection to a WebSocket for any requester.
* A malicious domain can successfully bind a socket using the victim's session cookies.
