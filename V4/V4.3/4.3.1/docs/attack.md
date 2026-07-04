# Attack Vectors for ASVS 4.3.1 (GraphQL DoS)

GraphQL shifts the power of query definition from the server to the client. This flexibility introduces a significant attack vector if queries are not constrained.

## Recursive Queries (Depth Exhaustion)
If the schema contains cyclical relationships (e.g., a `User` has `friends`, who are also `Users`), an attacker can craft a query that nests endlessly:
```graphql
query {
  users {
    friends {
      friends {
        friends {
          name
        }
      }
    }
  }
}
```
This forces the backend to resolve the database relationships recursively, exponentially increasing the workload and memory allocation until the server crashes.

## Resource Intensive Queries (Cost Exhaustion)
Even without deep recursion, requesting thousands of nodes and fields simultaneously (e.g., requesting 10,000 comments, their authors, and the author's profiles in a single shot) forces the server to do massive database joins and JSON serialization, locking up CPU threads and denying service to legitimate users.
