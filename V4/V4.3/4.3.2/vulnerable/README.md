# Vulnerable Implementation - ASVS 4.3.2

This application leaves GraphQL introspection enabled.
Attackers can send `__schema` queries to dump the entire API structure.
