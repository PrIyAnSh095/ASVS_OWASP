# Theoretical Background - ASVS 4.4.2

The Same-Origin Policy (SOP) is the fundamental security mechanism of the web, preventing one website from reading data from another. However, the WebSocket protocol (RFC 6455) was explicitly designed to allow cross-origin communication.

Because WebSockets bypass the SOP, the responsibility for securing them falls entirely on the server. When a browser initiates a WebSocket connection, it sends an HTTP request to upgrade the connection. It automatically includes:
1. The user's Cookies.
2. The `Origin` header (indicating where the script is hosted).

If a server does not check the `Origin` header, it assumes the request is legitimate. Because the cookies were sent, the connection is authenticated. This creates a severe vulnerability where an attacker can commandeer the user's session over a WebSocket, bypassing standard CSRF defenses.
