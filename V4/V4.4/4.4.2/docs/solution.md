# Solution Guide

To prevent Cross-Site WebSocket Hijacking (ASVS 4.4.2):

1. **Implement Origin Validation:** Always verify the `Origin` header during the HTTP Upgrade request.
2. **Use an Allowlist:** Never use wildcards (`*`) or regexes that can be bypassed (e.g., allowing `*example.com` which an attacker can bypass by registering `badexample.com`). Specify exact, trusted URLs.
3. **Framework Configuration:** Use built-in framework protections.
   * **Socket.IO (Python):** `SocketIO(app, cors_allowed_origins=["https://trusted.com"])`
   * **ws (Node.js):** Use the `verifyClient` callback to check `info.origin`.
4. **Token-Based Authentication:** As an additional defense, avoid relying solely on cookies. Require the client to send a unique session token or CSRF token over the WebSocket channel immediately after the connection is established.
