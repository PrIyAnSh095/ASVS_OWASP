# Theoretical Background - ASVS 4.3.1

GraphQL represents a paradigm shift from REST. Instead of the server dictating the shape and size of the response, the client requests exactly what it needs. While powerful for frontend developers, it is inherently dangerous for server stability.

## The N+1 Problem and Exponential Complexity
If an API exposes cyclical graphs, a simple 10-line query can trigger thousands of database calls. For example, requesting authors, their posts, those posts' comments, and the commenters' profiles.

Without defenses, GraphQL APIs are trivially susceptible to Application-Layer Denial of Service (DoS) attacks. Attackers don't need botnets; a single script sending complex queries can exhaust a database connection pool or OOM (Out of Memory) the application server.

ASVS 4.3.1 mandates that controls like Depth Limiting, Cost Analysis, or Allowlisting must be in place to cap the computational complexity an individual query can request.
