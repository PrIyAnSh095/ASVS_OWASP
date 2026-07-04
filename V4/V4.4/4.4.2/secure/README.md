# Secure Implementation - ASVS 4.4.2

This application strictly validates the `Origin` header during the initial WebSocket HTTP handshake.

## Security Control
By defining `cors_allowed_origins`, the server will only accept WebSocket upgrades if the request comes from an explicitly trusted site (e.g., `http://localhost:5000`). If a malicious site (`http://evil.com`) attempts to open a WebSocket connection to this server using the victim's browser, the server will reject the handshake, preventing Cross-Site WebSocket Hijacking (CSWSH).
