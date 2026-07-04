# Attack Vectors for ASVS 4.4.3 (WebSocket Authentication)

WebSockets present a unique challenge for authentication because they do not always easily inherit the standard HTTP session management controls (like `HttpOnly` cookies, depending on the client library or CORS configurations).

## Authentication Bypasses
If an application fails to securely authenticate a WebSocket connection:
1. **Missing Authentication:** An attacker can directly connect to `wss://api.example.com/stream` and start sending/receiving sensitive data without proving their identity.
2. **Weak Tokens:** If the WebSocket expects a token via a query parameter (e.g., `?token=123`) or initial payload, and the token is predictable, weak, or non-expiring, an attacker can guess it or steal it and use it forever.

## Impact
Unauthorized access to real-time data feeds, unauthorized execution of privileged commands via the WebSocket channel, and full session hijacking of the WebSocket context.
