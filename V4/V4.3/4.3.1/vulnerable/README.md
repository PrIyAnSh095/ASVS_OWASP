# Vulnerable Implementation - ASVS 4.3.1

This application provides a GraphQL API without any protection against expensive or deeply nested queries.

## The Vulnerability
GraphQL allows clients to specify exactly what data they want. Because the data model often contains recursive or cyclical relationships (e.g., `User` -> `friends` -> `User` -> `friends`), an attacker can request a massive amount of data in a single request. 

Since this server performs no Depth Limiting, Cost Analysis, or Allowlisting, it will attempt to fulfill arbitrarily large queries, leading to CPU and memory exhaustion (Denial of Service).
