# Expected Behavior

## Secure Implementation
* **AST Parsing Validation:** The server parses the incoming GraphQL query string into an Abstract Syntax Tree (AST) before executing it.
* **Depth & Cost Calculation:** The server traverses the AST to calculate the query's depth and assigned computational cost.
* **Enforcement:** If either the depth or cost limit is exceeded, the execution is halted immediately. A clear GraphQL error is returned to the user.
* **Resource Preservation:** The server remains available and responsive because malicious queries are dropped before interacting with the data layer.

## Vulnerable Implementation
* **Unrestricted Execution:** The server blindly executes any valid GraphQL query it receives.
* **Resource Exhaustion:** Deeply nested queries cause explosive data retrieval and serialization, dragging down CPU and memory.
* **Denial of Service:** Concurrently sending a few heavy queries will lock up the application's request threads, causing timeouts for other legitimate users.
