# Testing with Burp Suite

Since modern browsers do not allow JavaScript to spoof or modify the `Origin` header, you must use an intercepting proxy like Burp Suite to test for CSWSH vulnerabilities.

## Testing Steps
1. Open your browser and navigate to the target WebSocket application.
2. In Burp Suite, ensure Intercept is turned ON.
3. Click the "Connect" button in the application to initiate the WebSocket handshake.
4. In Burp Suite, locate the intercepted `GET` request containing `Upgrade: websocket`.
5. Find the `Origin` header (e.g., `Origin: http://localhost:5000`).
6. Change it to a malicious origin: `Origin: http://evil.com`.
7. Forward the request.

## Evaluating Results
* **PASS (Secure App):** The server returns an HTTP 400 Bad Request (or similar error) and the WebSocket connection fails. The server successfully validated the Origin.
* **FAIL (Vulnerable App):** The server returns an HTTP 101 Switching Protocols. The connection succeeds despite the malicious Origin.
