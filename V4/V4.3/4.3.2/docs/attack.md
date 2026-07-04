# Attack Vectors for ASVS 4.3.2 (GraphQL Introspection)

GraphQL introspection is a built-in feature that allows clients to query the server for its schema. 
While useful for development (e.g., auto-completion in GraphQL Playground), it is a massive information disclosure vulnerability in production.

## Exploitation
An attacker can send a single query requesting the `__schema` field. 
The server will respond with a full JSON representation of every Type, Field, Query, Mutation, and Argument available.

## Impact
This exposes hidden administrative endpoints, internal data structures, and deprecated/vulnerable fields. 
Attackers use this mapped surface to craft precise targeted attacks.
