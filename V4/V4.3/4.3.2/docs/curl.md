# Testing with cURL

You can use cURL to quickly verify if introspection is enabled.

## Test Command
```bash
curl -X POST http://localhost:5000/graphql \
-H "Content-Type: application/json" \
-d '{"query": "query { __schema { types { name } } }"}'
```

## Secure Response (PASS)
The secure application will return a `400 Bad Request` with an error message: `"GraphQL introspection is not allowed in production."`

## Vulnerable Response (FAIL)
The vulnerable application will return a `200 OK` dumping the available schema types, such as `Query`, `User`, `Post`, and `Comment`.
