# Expected Behavior

## Secure Implementation
* The user cannot obtain a WebSocket token without first possessing a valid HTTP session cookie.
* The WebSocket token is linked to the user's identity.
* The WebSocket connection is refused if the token is missing, expired, or previously used.
* Only the authenticated user can successfully upgrade to a WebSocket.

## Vulnerable Implementation
* The WebSocket endpoint can be accessed directly.
* Token endpoints (if they exist) issue valid tokens to unauthenticated users.
* The application fails to tie the WebSocket connection back to a securely authenticated HTTP session.
