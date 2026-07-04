# Theoretical Background - ASVS 4.2.5

The Open Worldwide Application Security Project (OWASP) Application Security Verification Standard (ASVS) Control 4.2.5 requires that applications restrict the size of generated URIs and HTTP headers when acting as an HTTP client.

## Why is this important?

When a web application interfaces with internal APIs or microservices, it acts as a client. If an attacker can control parts of the outgoing request—such as the path, query parameters, or specific headers (like Authorization tokens or custom correlation IDs)—they can inject massively oversized strings.

Web servers, proxies, and application frameworks have finite buffers for processing incoming HTTP requests. Common errors include:
* **HTTP 414 URI Too Long**
* **HTTP 431 Request Header Fields Too Large**

If the intermediate application does not enforce its own limits, an attacker can force the application to repeatedly generate enormous requests. This ties up thread pools, consumes memory, saturates network links, and causes denial of service in both the source application and the downstream infrastructure. Proper input validation and length restriction at the boundaries prevent these attacks.
