# Testing with Burp Suite

Burp Suite can be used to test the enforcement of the session transition logic.

## Testing Steps
1. **Unauthenticated Token Generation:** Send a `GET /api/ws-token` request in Burp Suite Repeater *without* any `Cookie` headers.
   * **FAIL:** The server issues a valid token.
   * **PASS:** The server returns a `401 Unauthorized`.
2. **Unauthenticated WS Connection:** Initiate a WebSocket connection (`GET /socket.io/?...`) without an auth payload or with a forged payload.
   * **FAIL:** The server returns `101 Switching Protocols` and allows interaction.
   * **PASS:** The server returns `400 Bad Request` or immediately closes the socket with an error frame.
