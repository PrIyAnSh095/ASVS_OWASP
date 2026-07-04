# Vulnerable Implementation - ASVS 4.4.4

This application fails to correctly transition an authenticated HTTPS session into a WebSocket session.

## Vulnerability
The application exposes a `/api/ws-token` endpoint that issues tokens without verifying the requester's HTTP session cookies. Furthermore, the WebSocket server itself does not rigorously validate the tokens upon connection. Consequently, an attacker can completely bypass the standard HTTPS authentication flow and immediately bind a WebSocket to interact with the backend API.
