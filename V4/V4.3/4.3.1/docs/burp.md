# Testing with Burp Suite

You can use Burp Suite to test a GraphQL endpoint for DoS vulnerabilities by sending deeply nested or highly complex payloads.

## Steps

1. **Intercept a GraphQL Request:** Find any request hitting `/graphql`. It will typically be a POST request with a JSON body containing `{"query": "..."}`.
2. **Send to Repeater:** Right-click and send the request to the Repeater tab.
3. **Modify the Query:**
   * Craft a deeply nested query exploiting cyclical relationships in the schema (e.g., user -> friends -> friends...).
   * Alternatively, request an excessive number of fields by using GraphQL aliases to request the same expensive field 100 times.
4. **Execute and Observe:**
   * **Secure Implementation:** Should immediately respond with a `400 Bad Request` or a GraphQL error object stating "Query exceeds maximum depth" or "Query exceeds maximum cost". The response time should be nearly instantaneous.
   * **Vulnerable Implementation:** The server will take a noticeably long time to respond, potentially timing out, crashing, or returning an enormous JSON payload. Sending multiple such requests concurrently will likely crash the service entirely.
