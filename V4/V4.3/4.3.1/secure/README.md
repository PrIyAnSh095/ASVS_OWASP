# Secure Implementation - ASVS 4.3.1

This application demonstrates a secure GraphQL API that enforces limits on queries to prevent Denial of Service (DoS).

## Security Controls Implemented
* **Depth Limiting:** The API parses the GraphQL AST and rejects any query with a nesting depth greater than 3. This prevents cyclical relationship exhaustion.
* **Cost Analysis:** The API assigns a basic cost to each requested field. If the total cost exceeds 20, the query is rejected.
* **Meaningful Errors:** Instead of executing and crashing, the server returns a 400 Bad Request with a clear message indicating which limit was breached.
