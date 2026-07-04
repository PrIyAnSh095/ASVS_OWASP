# Solution Guide

To secure a GraphQL API against expensive queries (ASVS 4.3.1), implement one or more of the following strategies:

1. **Depth Limiting:**
   * Use an AST parser or a middleware (like `graphql-depth-limit` in Node.js, or a custom AST visitor in Python) to calculate the maximum nesting depth of the query. Reject queries exceeding a reasonable threshold (e.g., 5).
2. **Query Cost Analysis:**
   * Assign point values to fields based on their computational expense. Sum the points before execution. Reject if the total exceeds a maximum allowed budget.
3. **Amount Limiting (Pagination limits):**
   * Enforce strict maximums on arguments like `first` or `limit` (e.g., `users(first: 100)`). Never allow unbounded lists.
4. **Query Allowlisting (Persisted Queries):**
   * If your API only serves your own frontends, pre-compile all legitimate queries and store their hashes on the server. The server should reject any query structure it hasn't seen before.
