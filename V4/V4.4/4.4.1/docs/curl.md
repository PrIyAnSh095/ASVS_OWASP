# Testing with cURL / CLI Tools

While `curl` is primarily for HTTP, you can use CLI tools like `wscat` to test WebSocket endpoints directly.

## Testing the Vulnerable Application (WS)
```bash
wscat -c ws://localhost:5000/chat
```
**Result:** The connection succeeds. Traffic is sent in plain text. (FAIL)

## Testing the Secure Application (WSS)
```bash
# Attempting plain WS on the secure port will fail
wscat -c ws://localhost:5000/chat

# Must use WSS (and --no-check since we use a self-signed cert for the lab)
wscat -c wss://localhost:5000/chat --no-check
```
**Result:** The secure server forces the use of TLS. Plain `ws://` connections are immediately rejected at the transport layer. (PASS)
