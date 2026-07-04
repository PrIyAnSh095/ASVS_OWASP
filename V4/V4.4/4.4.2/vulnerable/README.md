# Vulnerable Implementation - ASVS 4.4.2

This application fails to validate the `Origin` header during the initial WebSocket HTTP handshake.

## Vulnerability
By setting `cors_allowed_origins="*"` (or neglecting to check the origin entirely in native WebSocket implementations), the server accepts connections from any website. If a victim visits `http://evil.com`, the malicious site can establish a WebSocket connection to `http://localhost:5000` using the victim's browser. Because cookies (like session tokens) are automatically sent with the WebSocket handshake, the malicious site can interact with the server in the context of the authenticated user.
