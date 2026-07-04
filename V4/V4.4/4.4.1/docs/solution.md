# Solution Guide

To enforce secure WebSockets (WSS) and resolve ASVS 4.4.1:

1. **Frontend Update:** Ensure all client-side WebSocket initializations use the `wss://` protocol instead of `ws://`.
   ```javascript
   // Secure
   const socket = new WebSocket('wss://example.com/stream');
   ```
2. **Infrastructure Configuration:** Configure your web server, load balancer, or API gateway to terminate TLS (HTTPS). Disallow plain HTTP traffic or redirect it to HTTPS.
3. **Backend Enforcement (Optional but Recommended):** If your application is behind a proxy, read the `X-Forwarded-Proto` header. If it equals `http`, reject the WebSocket upgrade request.
