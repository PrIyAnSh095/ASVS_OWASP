# Solution Guide

To securely implement ASVS 4.4.3:

1. **Do Not Rely Exclusively on Query Parameters:** Avoid passing long-lived API keys or session tokens in the WebSocket URI (e.g., `ws://...?token=abc`), as URIs are logged in server access logs and proxy logs.
2. **Use Initial Payload Authentication:** Send the token inside the very first WebSocket frame after the connection is established (or via the `auth` payload supported by Socket.IO).
3. **Use Connection Tickets:**
   * Create an HTTP endpoint `/api/ws-ticket` protected by standard session cookies.
   * Generate a short-lived (e.g., 60 seconds), single-use cryptographic token.
   * Send the ticket to the client.
   * The client connects to the WebSocket and sends the ticket.
   * The server validates the ticket, links the WebSocket to the user's session, and invalidates the ticket.
