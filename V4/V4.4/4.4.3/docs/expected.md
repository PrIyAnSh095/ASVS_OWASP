# Expected Behavior

## Secure Implementation
* The server issues a long, cryptographically random string (e.g., a 256-bit hex token or a signed JWT) upon a successful HTTP login.
* The server records the expiration time of the token.
* The client passes the token securely (via the WS `auth` payload).
* The server strictly validates the token before allowing any business logic. Invalid tokens result in connection refusal.

## Vulnerable Implementation
* The server allows connections without checking for a token.
* Or, the server uses a static, hardcoded token (like `admin-token-123`) that never expires.
* An attacker can easily bypass authentication and access the WebSocket channel.
