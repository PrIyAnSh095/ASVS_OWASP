# Secure Implementation - ASVS 4.4.3

This application securely authenticates WebSocket connections using dedicated authentication tokens.

## How it works
1. When a user authenticates via standard HTTP (the `/login` endpoint), the server issues a cryptographically secure, random 256-bit token.
2. This token is stored on the server with a short expiration time (e.g., 30 seconds).
3. The client establishes the WebSocket connection and passes the token in the initial `auth` payload.
4. The server validates the token on the `connect` event. If the token is missing, invalid, or expired, the connection is instantly rejected with `ConnectionRefusedError`.
