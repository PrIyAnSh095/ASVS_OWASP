# Solution Guide

To satisfy ASVS 4.4.4, strictly link WebSocket access to the standard HTTP authentication flow:

1. **Protect Token Endpoints:** Ensure any endpoint issuing WebSocket tokens (like `/api/ws-token`) requires the standard HTTP session (e.g., `@login_required` or JWT validation).
2. **Issue Secure Tickets:** The token must be cryptographically random and explicitly mapped to the authenticated user on the backend.
3. **Validate on Connect:** When the WebSocket handshake occurs, intercept the token, validate it, and immediately invalidate the token so it cannot be reused.
4. **Link Identity:** Map the newly established WebSocket to the user identity found during ticket validation, so all subsequent WebSocket messages are processed in the context of that user.
