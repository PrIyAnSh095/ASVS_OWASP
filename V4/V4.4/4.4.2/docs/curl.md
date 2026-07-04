# Testing with cURL

You can use cURL to simulate the WebSocket handshake and observe the server's response to different `Origin` headers.

## Secure Implementation (Expected to Fail)
```bash
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
-H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
-H "Origin: http://evil.com" http://localhost:5000/socket.io/?EIO=4&transport=websocket
```
**Result:** HTTP 400 Bad Request. (The server rejects the untrusted origin).

## Vulnerable Implementation (Expected to Succeed)
```bash
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
-H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
-H "Origin: http://evil.com" http://localhost:5000/socket.io/?EIO=4&transport=websocket
```
**Result:** HTTP 101 Switching Protocols. (The server accepts the untrusted origin).
