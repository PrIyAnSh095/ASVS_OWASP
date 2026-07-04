# Testing with Burp Suite

Burp Suite fully supports WebSocket interception and allows you to easily verify if encryption is used.

## Steps
1. Configure your browser to proxy traffic through Burp Suite.
2. Navigate to the WebSocket application.
3. In Burp Suite, go to **Proxy > WebSockets history**.
4. Observe the captured WebSocket connections.

## FAIL Criteria (Vulnerable App)
If the URL in the history starts with `ws://`, the traffic is unencrypted. You can view the exact plain text messages sent in both directions.

## PASS Criteria (Secure App)
If the URL starts with `wss://`, the traffic is encrypted using TLS. Burp Suite can only see the plain text because it acts as a trusted TLS proxy (using its CA certificate installed in your browser). On the wire, outside of Burp, the traffic is heavily encrypted.
