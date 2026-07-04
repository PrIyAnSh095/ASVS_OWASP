# Testing with cURL / CLI

Because authentication happens during the Socket.IO protocol handshake or the initial WS payload, standard cURL is difficult to use for full validation. However, you can use CLI scripts or Postman's WebSocket interface.

To test manually:
1. Connect to the WebSocket endpoint.
2. Send an initial frame without the token payload.
3. Observe if the server closes the connection (Secure) or responds normally (Vulnerable).
