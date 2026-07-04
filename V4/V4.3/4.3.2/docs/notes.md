# Implementation Notes

* Most GraphQL frameworks (Apollo, Graphene, GraphQL-Java) enable introspection by default.
* Disabling it usually requires setting an explicit configuration flag (e.g., `introspection: false`) or adding a custom validation rule.
* In this lab, the secure application uses a simple string matching mechanism on the incoming query for educational clarity. In production, using the framework's native AST validation rules (`DisableIntrospectionRule`) is recommended.
