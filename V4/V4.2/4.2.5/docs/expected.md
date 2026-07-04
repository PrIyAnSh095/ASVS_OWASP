# Expected Behavior

## Secure Implementation
* **Validation:** Before constructing the outbound HTTP request, the length of the URI, Cookie, Authorization, and custom headers must be checked against strict maximum length limits.
* **Rejection:** If any limit is exceeded, the application must immediately return a descriptive error to the client (e.g., HTTP 400) without ever attempting to contact the downstream service.
* **Safe Forwarding:** Only requests within acceptable bounds are transmitted.

## Vulnerable Implementation
* **No Validation:** The application blindly takes user-provided strings and embeds them into outbound requests.
* **Downstream Errors:** Oversized payloads will reach the downstream target, triggering timeouts, 414 URI Too Long, or 431 Request Header Fields Too Large errors.
* **Resource Waste:** The vulnerable server wastes CPU, memory, and network resources dealing with arbitrarily large payloads.
