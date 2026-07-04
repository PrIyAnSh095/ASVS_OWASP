# Notes

- **ASVS 5.3.1 Requirement**: Verify that files uploaded or generated from untrusted user input and stored in a publicly accessible directory are never executed as server-side code when accessed directly through HTTP.
- **Simulation**: Since this lab runs on Flask (which doesn't natively execute `.php` or `.py` files in static directories like Apache does), the vulnerable version *simulates* a misconfiguration by explicitly checking for `.py` extensions and executing them via `subprocess`. This effectively demonstrates the core risk in a controlled manner.
