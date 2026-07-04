# Theoretical Background - ASVS 4.4.1

WebSockets (defined in RFC 6455) provide a full-duplex communication channel over a single TCP connection. 

## WS vs. WSS
The WebSocket protocol has two URI schemes:
* `ws://` operates over plain TCP (usually port 80). It is unencrypted.
* `wss://` (WebSocket Secure) operates over TLS (usually port 443). It provides the exact same encryption guarantees as HTTPS.

## Why WSS is Mandatory
Just like HTTP, plain WS traffic is vulnerable to Man-in-the-Middle (MitM) attacks. Because WebSockets are often used for highly sensitive, real-time data (like trading platforms, chat applications, and live notifications), ensuring Transport Layer Security (TLS) is critical to maintaining data confidentiality and integrity.
