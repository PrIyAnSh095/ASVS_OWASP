# Secure Implementation - ASVS 4.4.4

This application enforces a secure transition from an authenticated HTTPS session to a WebSocket channel.

## How it works
1. The user logs in via a standard `POST /login` request. The server issues a standard HTTP session cookie (e.g., `session`).
2. To open a WebSocket, the user makes an authenticated `GET /api/ws-token` request. The server verifies the HTTP session cookie and generates a single-use, short-lived cryptographic token (a "Connection Ticket").
3. The frontend initiates the WebSocket handshake, passing this specific token.
4. The WebSocket server validates the token, associates the socket with the authenticated user, and invalidates the token so it cannot be reused.
