# Testing with Burp Suite

You can use Burp Suite to manipulate the WebSocket connection parameters and test authentication controls.

## Testing Steps
1. Intercept the WebSocket connection request (the `GET` request upgrading the connection).
2. For Socket.IO v4, the authentication token is usually passed in the first WebSocket payload immediately after the HTTP upgrade, or as a query parameter in the handshake (e.g., `EIO=4&token=...`).
3. Attempt the following tests:
   * **Missing Token:** Delete the token parameter entirely and forward the request.
   * **Invalid Token:** Modify the token to random characters.
   * **Expired Token:** Wait 60 seconds and attempt to reconnect using the same token.

## Evaluating Results
* **PASS (Secure App):** The server refuses the connection or immediately closes the socket when invalid/expired/missing tokens are used.
* **FAIL (Vulnerable App):** The server establishes the connection and allows data exchange regardless of the token's state.
