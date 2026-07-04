# Implementation Notes

* In Python, `graphql-core` provides utilities (`parse` and `Visitor`) to analyze the AST of a query before handing it to the execution engine.
* **Query Cost:** In a production scenario, different fields should have different costs. Fetching a scalar string like `name` might cost 1, whereas fetching a computed relationship like `friends` might cost 10. The secure app demonstrates a simplified uniform cost model.
* **Persisted Queries / Allowlisting:** Another highly effective defense (especially for mobile/frontend apps with fixed queries) is to hash the queries on the frontend, register them on the backend, and only allow execution of known hashes. This completely neutralizes arbitrary complex queries from attackers.
