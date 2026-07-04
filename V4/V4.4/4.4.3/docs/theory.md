# Theoretical Background - ASVS 4.4.3

Authentication over WebSockets differs from REST APIs because WebSockets are stateful, persistent connections. 

Standard web applications use cookies for session management. However, WebSockets often reside on subdomains or cross-origin environments where standard cookies are not available or are blocked by browser security policies. Furthermore, non-browser clients (like mobile apps) don't manage cookies natively.

When an application falls back to alternative session management for WebSockets, developers often make fatal errors, such as using predictable tokens, non-expiring tokens, or skipping authentication entirely. ASVS 4.4.3 requires that any dedicated WebSocket token must possess the same security guarantees as a standard HTTP session identifier (entropy, uniqueness, unpredictability, and expiration).
