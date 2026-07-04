# Theoretical Background - ASVS 4.4.4

Modern applications often use dual architectures: an HTTP REST API for standard CRUD operations and a WebSocket server for real-time pub/sub functionality. 

Because standard HTTP session management relies heavily on cookies, transitioning that authenticated state to a separate protocol (WebSockets) requires careful engineering. Browsers often handle cross-domain cookies poorly during WebSocket upgrades, and non-browser clients (like mobile apps) don't use cookies natively.

Therefore, the most secure mechanism is to use the proven HTTP session to request a dedicated WebSocket token. This proves the client was authenticated in the HTTP realm before allowing them to transition into the WebSocket realm, maintaining a continuous chain of trust.
