# Attack Vectors for ASVS 4.4.4 (Session Transition Bypass)

When applications use WebSockets for authenticated data feeds, attackers will look for ways to connect to the WebSocket directly, bypassing the traditional HTTP login flow.

## The Disconnect Between HTTP and WebSockets
Because WebSockets operate on a different protocol layer and often sit on different infrastructure (like a separate microservice), they frequently lack access to the primary HTTP session state (e.g., memory-backed sessions or Redis session stores). 

## Exploitation
If the WebSocket endpoint fails to mandate a cryptographically secure token *that was issued exclusively to a verified HTTP session*, an attacker can:
1. Connect directly to the WebSocket URL using `wscat` or a script.
2. If tokens are required but issued indiscriminately via an unauthenticated REST endpoint (e.g., `/api/get-token`), the attacker requests a token and connects.
3. Access real-time data or dispatch commands that should have required a valid user session.
