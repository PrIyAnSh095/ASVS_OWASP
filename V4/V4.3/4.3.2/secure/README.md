# Secure Implementation - ASVS 4.3.2

This application disables GraphQL introspection.
It intercepts incoming queries and rejects those containing `__schema` or `__type` meta-fields.
This prevents attackers from discovering internal data models and available operations.
