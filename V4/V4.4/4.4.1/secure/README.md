# Secure Implementation - ASVS 4.4.1

This application enforces WebSocket over TLS (WSS).
It uses an ad-hoc SSL context to bind to HTTPS, ensuring that any WebSocket connection made to `/chat` uses the encrypted `wss://` protocol. 
Any attempt to connect via plain `ws://` to this port will fail at the transport layer, effectively securing the data in transit.
