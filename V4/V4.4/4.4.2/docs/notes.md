# Implementation Notes

* `Flask-SocketIO` manages CORS and Origin validation natively via the `cors_allowed_origins` parameter. Setting this to a specific list completely mitigates CSWSH.
* If you are writing a raw WebSocket server using `websockets` or `flask-sock`, you must manually extract the `Origin` header from the handshake request and validate it before accepting the socket.
* **Important:** CSWSH only affects WebSocket endpoints that rely on ambient credentials (like cookies or HTTP Basic Auth) for authentication. If the endpoint requires a token to be sent inside the WebSocket payload (e.g., a Bearer token in the first frame), the impact of CSWSH is neutralized because the attacker on `evil.com` cannot access the token to send it. However, ASVS still mandates Origin validation as a defense-in-depth measure.
