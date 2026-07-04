# Testing with Burp Suite

You can easily discover if a GraphQL endpoint has introspection enabled using Burp Suite.

## Discovery
1. Intercept any GraphQL POST request in Burp Suite Proxy.
2. Send the request to Repeater.
3. Replace the `query` field in the JSON body with a standard introspection payload (e.g., requesting `__schema { types { name } }`).
4. If the server responds with a 200 OK and a list of types, introspection is enabled (FAIL).
5. If the server responds with an error indicating introspection is disabled, the control is met (PASS).

*Burp Suite Extensions like InQL can automate this process.*
