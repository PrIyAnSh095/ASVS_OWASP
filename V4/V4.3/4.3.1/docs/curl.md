# Testing with cURL

You can use cURL to send malicious GraphQL payloads from the command line to test for depth limits.

## Secure App Test
```bash
curl -X POST http://localhost:5000/graphql \
-H "Content-Type: application/json" \
-d '{"query": "{ users { friends { friends { friends { friends { name } } } } } }"}'
```
**Expected Result:** The server parses the AST, calculates the depth, and immediately returns an error indicating the maximum depth (e.g., 3) was exceeded.

## Vulnerable App Test
```bash
curl -X POST http://localhost:5000/graphql \
-H "Content-Type: application/json" \
-d '{"query": "{ users { friends { friends { friends { friends { friends { friends { friends { name } } } } } } } } }"}'
```
**Expected Result:** The server executes the entire query, returning a massive, deeply nested JSON response, consuming significant backend resources.
