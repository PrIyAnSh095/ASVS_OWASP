# Theoretical Background - ASVS 4.3.2

GraphQL is strongly typed and self-documenting. Introspection is the mechanism that powers this self-documentation.

## Security vs. Usability
In development, introspection is vital for IDE auto-completion and tools like GraphiQL. 
In production, it violates the principle of "Security through Obscurity" – though obscurity is not a primary defense, freely handing an attacker a complete map of your API greatly accelerates their reconnaissance phase.

ASVS 4.3.2 mandates disabling this feature in production to force attackers to guess or reverse-engineer the schema, significantly raising the barrier to entry for exploiting other vulnerabilities.
