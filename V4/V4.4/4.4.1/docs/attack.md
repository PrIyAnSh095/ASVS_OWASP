# Attack Vectors for ASVS 4.4.1 (Insecure WebSockets)

WebSockets provide a persistent, bidirectional communication channel. If this channel is not encrypted (using `ws://` instead of `wss://`), it is vulnerable to network-level attacks.

## Man-in-the-Middle (MitM) Attacks
Because `ws://` traffic is transmitted in clear text, an attacker positioned on the same network (e.g., a public Wi-Fi hotspot, compromised router, or malicious ISP) can intercept the traffic.

## Impact
* **Eavesdropping:** Attackers can read sensitive data such as chat messages, session tokens, financial tickers, or personal user information as it flows across the WebSocket.
* **Data Tampering:** Attackers can inject their own WebSocket frames or modify existing frames in transit, altering the data received by the client or the server without either party knowing.
