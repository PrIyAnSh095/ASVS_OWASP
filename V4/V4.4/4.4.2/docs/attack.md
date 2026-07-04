# Attack Vectors for ASVS 4.4.2 (CSWSH)

Cross-Site WebSocket Hijacking (CSWSH) is the WebSocket equivalent of Cross-Site Request Forgery (CSRF).

## Mechanism
When a browser opens a WebSocket connection, it performs an initial HTTP GET request with an `Upgrade: websocket` header. Crucially, the browser automatically attaches any cookies associated with the target domain (e.g., session cookies) and automatically sets the `Origin` header to the site hosting the JavaScript that initiated the connection.

## Exploitation
1. A victim logs into the vulnerable application (e.g., a banking site with a live WebSocket feed).
2. The victim is lured to `http://evil.com`.
3. `evil.com` executes JavaScript: `new WebSocket('ws://bank.com/feed')`.
4. The victim's browser sends the request to `bank.com`, attaching the victim's banking session cookies. The browser also sets `Origin: http://evil.com`.
5. If `bank.com` does not validate the `Origin` header, it accepts the connection.
6. The attacker on `evil.com` now has a persistent, two-way communication channel with the bank server, authenticated as the victim, allowing them to read sensitive data or execute actions.
