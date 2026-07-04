# Expected Behavior

## Secure Implementation
* The server binds to a secure port and requires a TLS handshake before establishing a WebSocket connection.
* The frontend initiates connections exclusively using the `wss://` URI scheme.
* Any attempt to connect using `ws://` is rejected.
* All data frames are encrypted over the network.

## Vulnerable Implementation
* The server binds to a standard HTTP port.
* The frontend initiates connections using the `ws://` URI scheme.
* Data frames are transmitted in clear text, exposing them to eavesdropping and tampering.
