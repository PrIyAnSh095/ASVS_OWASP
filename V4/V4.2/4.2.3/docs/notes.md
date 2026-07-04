# ASVS 4.2.3 - Additional Notes and References

## Overview

This document contains additional context, references, and practical notes for ASVS 4.2.3 implementation.

## HTTP/2 RFC References

### RFC 7540 - Hypertext Transfer Protocol Version 2

- **Full Title:** Hypertext Transfer Protocol Version 2 (HTTP/2)
- **Status:** Proposed Standard
- **Publication:** May 2015
- **Key Section:** [8.1.2 Connection-Specific Header Fields](https://tools.ietf.org/html/rfc7540#section-8.1.2)

**Exact Quote from RFC 7540 Section 8.1.2:**
> "HTTP/2 uses the ":" notation and pseudo-header field names to convey the target URI, method, and other parts of the request and response message. These ":" pseudo-header field names are:
> 
> ...
> 
> A sender MUST NOT generate a message containing a header field with a name that contains a character that is not permitted in a header field name. When a request message is converted from HTTP/1.1, a sender MUST:
>
> - Remove the Connection header field (Section 7.6.1 of [RFC7230]), along with any header fields referenced by it (that is, Proxy-Connection, Keep-Alive, Transfer-Encoding, and Upgrade);
> - Replace the Transfer-Encoding header field with its decoded equivalent...
> - Remove any header fields with names that are not valid..."

### Related RFCs

- **RFC 7230:** HTTP/1.1 Message Syntax and Routing (obsolete but referenced)
- **RFC 7231:** HTTP/1.1 Semantics and Content (obsolete but referenced)
- **RFC 7540:** HTTP/2 Specification (current standard)
- **RFC 7541:** HPACK - HTTP/2 Header Compression
- **RFC 7541 (HTTP/3):** Work in progress for HTTP/3

## Historical Context

### Why These Headers Existed in HTTP/1.1

| Header | Purpose | HTTP/1.1 Use Case |
|--------|---------|------------------|
| Connection | Manage connection state | Close or keep-alive persistence |
| Keep-Alive | Specify timeout and max requests | Tune connection reuse |
| Transfer-Encoding | Frame data using chunked encoding | Send response before size known |
| Upgrade | Suggest protocol upgrade | HTTP → WebSocket, HTTP → HTTPS |
| Proxy-Connection | Non-standard, like Connection | Some proxies used this |
| Trailer | Declare trailers in body | Send headers after body for integrity checking |

### Evolution of Handling

```
HTTP/1.0 (1996)
├─ Simple request-response
└─ Connection closed after each request

HTTP/1.1 (1997)
├─ Persistent connections (keep-alive)
├─ Pipelining (limited)
├─ Chunked transfer encoding
├─ Upgrade mechanism
└─ These headers become important

HTTP/2 (2015)
├─ Multiplexing over single connection
├─ Binary framing with explicit lengths
├─ No concept of "connection persistence" negotiation
├─ Headers forbidden (MUST NOT)
└─ Cleaner protocol

HTTP/3 (2022)
├─ Built on QUIC (UDP-based)
├─ Already HTTP/2-like framing
├─ Continues HTTP/2 header rules
└─ Forbidden headers carry forward
```

## Implementation Notes

### Language-Specific Considerations

#### Python (Flask)

**Header access:**
```python
# Headers in Flask
request.headers.get('Transfer-Encoding')  # Case-insensitive
request.headers['Transfer-Encoding']       # Case-insensitive, raises KeyError
dict(request.headers)                      # All headers as dict
```

**Protocol detection:**
```python
# HTTP version in Flask
request.environ.get('SERVER_PROTOCOL')  # 'HTTP/2', 'HTTP/1.1', etc.
request.environ.get('wsgi.url_scheme')  # 'http' or 'https'
```

#### Node.js (Express)

**Header access:**
```javascript
// Headers in Express
req.get('Transfer-Encoding')         // Case-insensitive
req.headers['transfer-encoding']     // Case-sensitive
Object.keys(req.headers)             // All header names (lowercase)
```

**Protocol detection:**
```javascript
// HTTP version in Express/Node
req.httpVersion              // '2.0', '1.1', '1.0'
req.connection.alpnProtocol  // 'h2', 'http/1.1', etc.
```

#### Java (Spring)

**Header access:**
```java
// Headers in Spring
request.getHeader("Transfer-Encoding")    // Case-insensitive
request.getHeaderNames()                  // Enumeration
request.getHeaders("Transfer-Encoding")   // Multiple values
```

**Protocol detection:**
```java
// HTTP version in Spring
request.getProtocol()         // "HTTP/2.0", "HTTP/1.1"
request.getScheme()           // "http", "https"
```

#### Go (net/http)

**Header access:**
```go
// Headers in Go
r.Header.Get("Transfer-Encoding")    // Case-insensitive
r.Header["Transfer-Encoding"]        // Direct access (lowercase)
r.Header.Values("Transfer-Encoding") // Multiple values
```

**Protocol detection:**
```go
// HTTP version in Go
r.Proto              // "HTTP/1.1", "HTTP/2.0"
r.ProtoMajor, r.ProtoMinor // 2, 0 for HTTP/2
```

### Reverse Proxy Considerations

#### Nginx

**Current HTTP/2 Support:** ✓ Full support

**Default Behavior:** Nginx already filters these headers when acting as proxy

**Configuration:**
```nginx
# Explicit rejection
if ($http_transfer_encoding) { return 400; }
if ($http_connection) { return 400; }

# Or proxy configuration
proxy_pass_request_headers off;  # Filter all headers
proxy_set_header X-Forwarded-For $remote_addr;
```

#### Apache mod_http2

**Current HTTP/2 Support:** ✓ Full support

**Default Behavior:** Apache filters these headers

**Configuration:**
```apache
# HTTP/2 header filtering
H2Upgrade on
H2Direct on
```

#### HAProxy

**Current HTTP/2 Support:** ✓ Full support (v1.8+)

**Configuration:**
```
frontend http2
    bind :443 ssl alpn h2,http/1.1
    
    # Strip connection-specific headers
    http-request del-header Transfer-Encoding
    http-request del-header Connection
    http-request del-header Keep-Alive
```

### Container/Orchestration Notes

#### Docker

**Image Selection for HTTP/2:**
- Base image with h2 support (hypercorn, nghttp2)
- Avoid images with only HTTP/1.1 support

**Dockerfile:**
```dockerfile
# Good: Has HTTP/2
FROM python:3.11-slim
RUN pip install hypercorn h2

# Avoid: No HTTP/2
FROM python:3.11-slim
RUN pip install gunicorn  # Only HTTP/1.1
```

#### Kubernetes

**Service Configuration:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  ports:
  - name: http2
    port: 443
    targetPort: 8443
    protocol: TCP
```

**Ingress:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - example.com
    secretName: example-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              name: http2
```

## Security Considerations

### Attack Complexity

| Attack | Complexity | Prerequisites |
|--------|-----------|----------------|
| Header Injection | LOW | HTTP/2 app accepting headers |
| Response Splitting | LOW | Headers reflected in response |
| Request Smuggling | MEDIUM | HTTP/2 to HTTP/1.1 proxy setup |
| Cache Poisoning | MEDIUM | Caching layer misconfiguration |
| Protocol Confusion | MEDIUM | Multiple protocol layers |

### Real-World Scenarios

**Scenario 1: Cloud Microservices**
```
User → CDN (HTTP/2) → Load Balancer (HTTP/2) → Backend (HTTP/1.1)
└─ Vulnerable app accepts Transfer-Encoding
   ├─ CDN normalizes to HTTP/2 (strips header)
   ├─ Load balancer forwards to backend
   ├─ Backend sees Transfer-Encoding → confused parsing
   └─ Request smuggling possible
```

**Scenario 2: API Gateway**
```
Client (HTTP/2) → API Gateway (HTTP/2) → Backend (HTTP/1.1)
└─ Gateway doesn't validate
   ├─ Client sends: Transfer-Encoding: chunked
   ├─ Gateway forwards to backend
   ├─ Backend processes differently
   └─ Desynchronization = potential exploit
```

**Scenario 3: CDN Cache Poisoning**
```
Attacker (HTTP/2) → CDN (Cache) → Users (HTTP/2)
└─ Injects malicious headers
   ├─ CDN caches response with injected headers
   ├─ Users receive poisoned cache entry
   ├─ Headers reflect in response to users
   └─ XSS or credential theft possible
```

## Compliance Mapping

### ASVS Level 3

ASVS 4.2.3 is a **Level 3** control, required for:
- High-assurance applications
- Financial systems
- Healthcare systems
- Government systems
- Critical infrastructure

### Related Controls

| Control | Relationship |
|---------|--------------|
| ASVS 4.1.1 | General request validation |
| ASVS 4.1.2 | Content-Type validation |
| ASVS 4.1.3 | URL validation |
| ASVS 4.2.1 | HTTP method validation |
| ASVS 4.2.2 | HTTP status code validation |
| ASVS 4.2.3 | **THIS CONTROL** - HTTP/2 headers |
| ASVS 5.2.1 | CORS policy enforcement |

### CWE Mapping

| CWE | Title | Relevance |
|-----|-------|-----------|
| CWE-113 | Improper Neutralization of CRLF Sequences | Header injection |
| CWE-444 | Inconsistent Interpretation of HTTP Requests | Request smuggling |
| CWE-441 | Unintended Proxy or Intermediary | Request confusion |
| CWE-645 | Overly Restrictive Quoting of Special Characters | Header parsing |

### OWASP Top 10 Mapping

| OWASP | Category | Relevance |
|-------|----------|-----------|
| A01:2021 | Broken Access Control | Protocol confusion bypass |
| A02:2021 | Cryptographic Failures | Protocol downgrade |
| A03:2021 | Injection | Header injection |
| A05:2021 | Security Misconfiguration | Protocol mismatch |
| A06:2021 | Vulnerable and Outdated Components | Outdated header handling |

## Testing Tools

### Recommended Tools

| Tool | Purpose | HTTP/2 Support |
|------|---------|----------------|
| Burp Suite | Comprehensive testing | Excellent |
| OWASP ZAP | Security scanning | Good |
| curl | CLI testing | Limited (version dependent) |
| http2-cli | CLI specifically for HTTP/2 | Excellent |
| nghttp2 | HTTP/2 client library | Excellent |
| Python h2 | HTTP/2 library | Excellent |
| Node.js http2 | Native HTTP/2 | Excellent |
| Go net/http2 | Native HTTP/2 | Excellent |

### Burp Suite Extensions

- **HTTP/2 Enhancements:** Better HTTP/2 support
- **Active Scan:** Includes HTTP/2 checks
- **Intruder:** Can test with HTTP/2

### Custom Testing Scripts

**Python with http.client:**
```python
import http.client

# Connect with HTTP/2
conn = http.client.HTTPConnection('localhost:8000')

# Add forbidden header
headers = {'Transfer-Encoding': 'chunked'}

# Send request
conn.request('POST', '/api/test', headers=headers)
response = conn.getresponse()

print(f"Status: {response.status}")
print(response.read().decode())
```

**Node.js with http2:**
```javascript
const http2 = require('http2');

const client = http2.connect('http://localhost:8000');

const req = client.request({
  ':path': '/api/test',
  ':method': 'POST',
  'transfer-encoding': 'chunked'
});

req.on('response', (headers) => {
  console.log(headers);
});

req.end();
```

## Performance Impact Analysis

### Validation Overhead

**Header checking cost:**
- Set membership test: O(1) average case
- Header iteration: O(n) where n = number of headers
- Total: ~1-5ms for typical requests

**Optimization:**
```python
# Fast path for HTTP/1.1
if not is_http2:
    return  # Skip validation entirely

# Only validate HTTP/2
# ...
```

### Caching Strategy

```python
# Cache validation result to avoid repeated checks
VALIDATION_CACHE = {}

def get_cached_validation(request_headers_hash):
    return VALIDATION_CACHE.get(request_headers_hash)

def cache_validation(request_headers_hash, result):
    VALIDATION_CACHE[request_headers_hash] = result
```

## Troubleshooting Guide

### Symptom: Valid requests rejected

**Possible causes:**
1. Header name case sensitivity issue
2. Protocol detection incorrect
3. Whitespace in header names

**Solution:**
```python
# Ensure case-insensitive comparison
if header_name.lower() in FORBIDDEN_HTTP2_HEADERS:
    # Reject
```

### Symptom: No HTTP/2 detection

**Possible causes:**
1. Server not using HTTP/2
2. Protocol detection code broken
3. Client not actually using HTTP/2

**Debug:**
```python
print(f"Protocol: {request.environ.get('SERVER_PROTOCOL')}")
print(f"Headers: {dict(request.headers)}")
```

### Symptom: Proxy bypasses validation

**Possible causes:**
1. Proxy adds/removes headers
2. Validation only at one layer
3. Different proxy handling

**Solution:**
1. Validate at multiple layers
2. Configure proxy correctly
3. Use defense in depth

## Maintenance and Updates

### Regular Reviews

**Frequency:** Quarterly

**Checklist:**
- [ ] RFC 7540 for updates
- [ ] CWE/CVSS for new vulnerabilities
- [ ] Framework security advisories
- [ ] Reverse proxy version updates
- [ ] Testing tool updates

### Logging Best Practices

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Log attempts
logger.warning(f"Forbidden HTTP/2 header attempt: {header} from {request.remote_addr}")

# Log policy enforcement
logger.info(f"HTTP/2 request accepted - compliant with ASVS 4.2.3")

# Log errors
logger.error(f"Header validation error: {str(e)}")
```

### Monitoring Metrics

**Track:**
- Requests with forbidden headers (per day/hour)
- Rejection rate by header type
- Source IPs attempting violations
- False positive rate
- Validation latency

```python
# Prometheus metrics example
from prometheus_client import Counter, Histogram

forbidden_header_counter = Counter(
    'forbidden_headers_total',
    'Total forbidden HTTP/2 headers detected',
    ['header_name']
)

validation_latency = Histogram(
    'validation_duration_seconds',
    'Header validation duration'
)
```

## FAQ

**Q: Does this break backward compatibility?**
A: Only for applications explicitly sending these headers in HTTP/2 (rare). HTTP/1.1 is unaffected.

**Q: Why not just strip the headers?**
A: Stripping could hide attacks. Rejecting is more secure and explicit.

**Q: What about CDNs and proxies?**
A: Most modern CDNs (Cloudflare, AWS CloudFront) already enforce this. Application-level enforcement adds defense in depth.

**Q: Is HTTP/1.1 affected?**
A: No, validation only triggers for HTTP/2 requests.

**Q: Can I disable this for backward compatibility?**
A: Possible but not recommended. Consider:
1. Version API endpoints
2. Feature flags for gradual rollout
3. Client communication strategy

**Q: What about custom headers?**
A: Only the 6 RFC-forbidden headers are checked. Custom headers are allowed.

## Resources

### Online Resources

- [OWASP HTTP/2 Security](https://owasp.org/www-community/attacks/HTTP_Response_Splitting)
- [RFC 7540 Specification](https://tools.ietf.org/html/rfc7540)
- [HTTP/2 Explained](https://http2explained.haxx.se/)
- [Burp Suite HTTP/2 Testing](https://portswigger.net/burp)

### Books

- "HTTP/2 in Action" by Barry Pollard
- "Web Security Testing Cookbook" by Paco Hope and Ben Walther
- "The Web Application Hacker's Handbook" (2nd Edition)

### Papers

- "HTTP Request Smuggling" - James Kettle
- "Request smuggling, cache poisoning and other chimeras" - Alchemy Security

## Conclusion

ASVS 4.2.3 addresses a critical security gap in HTTP/2 implementations. By understanding the historical context, attack vectors, and proper remediation, you can build secure, compliant applications.

**Key Takeaways:**
1. HTTP/2 forbids 6 connection-specific headers per RFC 7540
2. Accepting them enables header injection, smuggling, and splitting attacks
3. Early validation is essential
4. Monitor and log all attempts
5. Defense in depth across all layers (proxy, gateway, application)
6. Keep frameworks and dependencies updated

For questions or updates, refer to RFC 7540 and OWASP resources.
