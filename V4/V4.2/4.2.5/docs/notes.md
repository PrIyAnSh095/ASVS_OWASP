# Implementation Notes

* The secure application enforces limits using Python's `len(string.encode('utf-8'))` to accurately measure byte length, not just character length. This prevents bypasses using multi-byte characters.
* Real-world applications should define these limits based on the actual capacities of downstream components (e.g., AWS API Gateway limits, NGINX `large_client_header_buffers`, etc.).
* It is highly recommended to combine size limits with proper character sanitization (e.g., rejecting newline characters in headers to prevent HTTP Request Smuggling or Header Injection). While this lab focuses on length (4.2.5), sanitization is equally critical.
