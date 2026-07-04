# Attack Vectors for ASVS 4.2.5

When applications dynamically construct outbound requests (such as server-side requests to internal APIs or microservices) based on user input, attackers can exploit this behavior if no length validation is enforced.

## Mechanism

If an attacker supplies excessively large inputs (e.g., hundreds of megabytes) into fields that are subsequently used as URI paths or HTTP headers (Cookie, Authorization, etc.), the application may:
1. Allocate excessive memory to hold the string.
2. Send the bloated request over the network, consuming bandwidth.
3. Overwhelm the downstream service, which might crash, hang, or return errors when trying to parse an unusually large HTTP header or URI.

This chain of events can cause Denial of Service (DoS) across multiple layers of the application infrastructure.

## Impact

* **Memory Exhaustion:** Both the frontend/backend creating the request and the downstream component receiving it might run out of memory.
* **Network Congestion:** Massive requests can tie up network connections.
* **Component Failures:** Web servers like NGINX or Apache have default limits for headers and URIs (e.g., `large_client_header_buffers`). Exceeding these causes HTTP 414 (URI Too Long) or 431 (Request Header Fields Too Large) errors, effectively breaking the downstream process.
