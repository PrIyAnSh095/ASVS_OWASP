# Expected Behavior

## Secure Implementation
* Introspection queries containing `__schema` or `__type` are intercepted and rejected.
* A clear error message is returned.
* Standard application queries (e.g., fetching users) continue to function normally.

## Vulnerable Implementation
* Introspection queries are processed.
* The API returns its complete schema definition upon request, aiding attackers in reconnaissance.
