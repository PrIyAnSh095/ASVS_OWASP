# ASVS 4.2.3 Attack Vectors and Exploitation

## Overview

This document details the specific attack vectors that ASVS 4.2.3 is designed to prevent. Understanding these attacks is crucial for implementing proper defense mechanisms.

## Table of Contents

1. [Header Injection](#header-injection)
2. [Response Splitting](#response-splitting)
3. [Request Smuggling](#request-smuggling)
4. [Cache Poisoning](#cache-poisoning)
5. [Protocol Confusion](#protocol-confusion)
6. [Exploitation Chains](#exploitation-chains)
7. [Detection and Defense](#detection-and-defense)

## Header Injection

### Mechanism

Header injection exploits improper handling of header values that contain CRLF (Carriage Return Line Feed: `\r\n`) sequences. In HTTP, CRLF marks the end of each line.

### Attack Format

```
Original Intent:
  User-Agent: Mozilla/5.0

Attacker Payload:
  User-Agent: Mozilla/5.0\r\nX-Injected-Header: malicious-value

Result (if vulnerable):
  User-Agent: Mozilla/5.0
  X-Injected-Header: malicious-value
```

### Example 1: Basic Header Injection

```http
GET / HTTP/2
Host: example.com
Transfer-Encoding: chunked\r\nContent-Length: 0

# If headers are echoed or forwarded without sanitization:
Transfer-Encoding: chunked
Content-Length: 0  # <-- Injected
```

### Example 2: Authentication Header Injection

```http
POST /api/balance HTTP/2
Host: bank.example.com
Authorization: Bearer user-token\r\nX-Admin: true

# If application checks X-Admin header without proper scope:
Authorization: Bearer user-token
X-Admin: true  # <-- Attacker gained admin flag
```

### Example 3: Cache Header Injection

```http
GET /user/profile HTTP/2
Host: example.com
Cache-Control: public\r\nVary: Accept-Encoding,X-Forwarded-For

# Backend cache (Varnish, Redis) sees:
# Key includes: Vary: Accept-Encoding,X-Forwarded-For
# Attacker can poison for specific X-Forwarded-For values
```

### Attack Prerequisites

1. Application accepts and processes HTTP/2 requests
2. Application forwards headers without sanitization
3. Downstream system interprets injected headers
4. Injected header affects decision-making

### Impact Scenarios

| Scenario | Attack | Impact |
|----------|--------|--------|
| Authentication | Inject authorization headers | Bypass authentication |
| Authorization | Inject role/admin headers | Escalate privileges |
| Cache | Inject cache-control headers | Cache poisoning |
| Request routing | Inject routing headers | Route to unintended backend |
| Backend confusion | Inject content-type | Content type confusion |

## Response Splitting

### Mechanism

Response splitting allows attacker to inject an entire HTTP response, including status line, headers, and body. This is a more severe form of header injection.

### Attack Format

```
Attacker Input:
  Header-Value: value\r\n\r\n<injected HTTP response>

Result:
  Header-Value: value

  <injected HTTP response>
```

### Example 1: Basic Response Splitting

```http
# Vulnerable Application Code:
response.add_header("Content-Type", request.get_param("type"))

# Attacker Parameter:
type=text/html\r\n\r\n<html><body>Phishing Content</body></html>

# Resulting Response:
HTTP/2 200 OK
Content-Type: text/html

<html><body>Phishing Content</body></html>
```

### Example 2: Injecting Redirect

```http
# Attacker crafts:
Transfer-Encoding: chunked\r\n\r\nHTTP/2 302 Found\r\nLocation: http://attacker.com\r\n\r\n

# Two responses are created:
Response 1: 302 Found, redirect to attacker.com
Response 2: Original intended response
```

### Example 3: XSS via Response Splitting

```http
# Attacker parameter:
id=123\r\n\r\n<html><script>alert('XSS')</script></html>

# Browser receives:
HTTP/2 200 OK
Content-Type: application/json

<html><script>alert('XSS')</script></html>
# Browser interprets as HTML/JavaScript due to injected content
```

### Attack Prerequisites

1. Application reflects user input in HTTP headers
2. Application doesn't validate/sanitize user input
3. Client accepts multiple responses from single connection
4. Client doesn't validate response headers

### Impact

- **Phishing:** Redirect users to attacker site
- **XSS:** Inject and execute arbitrary JavaScript
- **Session Hijacking:** Set cookies to capture sessions
- **Cache Poisoning:** Inject responses into cache
- **Worm Spread:** Self-propagating via reflected responses

## Request Smuggling

### Mechanism

Request smuggling exploits different interpretation of HTTP message boundaries between client, proxy, and backend server. HTTP/2 multiplexing exacerbates this.

### HTTP/1.1 Request Smuggling Foundation

In HTTP/1.1, message boundaries are determined by:
1. `Content-Length` header
2. `Transfer-Encoding` header
3. Connection closure

If different parties disagree on message boundaries, smuggling occurs.

```
Proxy interprets as:  Request 1
                      Request 2

Backend interprets as: Request 1+2 (invalid)
                      Request 3 (attacker's smuggled request)
```

### Example 1: Transfer-Encoding vs Content-Length Confusion

```http
# Attacker crafts to HTTP/2 proxy that validates but forwards to HTTP/1.1 backend:

POST /transfer HTTP/2
Host: bank.example.com
Content-Length: 100
Transfer-Encoding: chunked

# HTTP/2 proxy: Validates, sees frame boundary (explicit length)
# Forwards with Content-Length=100

# HTTP/1.1 backend: Prioritizes Transfer-Encoding over Content-Length
# Processes chunked body
# Different boundary interpretation = smuggling
```

### Example 2: Multiple Transfer-Encoding Directives

```http
POST /api HTTP/2
Transfer-Encoding: chunked
Transfer-Encoding: gzip

# Some implementations process first: chunked
# Others process last: gzip
# Results in different boundary interpretation
```

### Example 3: Whitespace in Transfer-Encoding

```http
POST / HTTP/2
Transfer-Encoding: chunked \r\n
Transfer-Encoding: identity

# Some implementations ignore second directive
# Others prioritize later directive
# Causes boundary confusion
```

### Example 4: Prefix Smuggling Attack

```http
# Step 1: Attacker sends request that's partially valid
POST /api/transfer HTTP/2
Transfer-Encoding: chunked
Content-Length: 150

# Payload designed so:
# - HTTP/2 layer sees frame boundary (legitimate)
# - HTTP/1.1 backend sees content-length boundary differently
# - Attacker crafts payload to smuggle:

G  # Start of chunk "GET /admin HTTP/1.1\r\n..."
E
T
...
# When decoded: Becomes GET /admin request

# Victim's next legitimate request:
POST /api/data HTTP/1.1
...

# Backend sees smuggled request + victim request as one message
# Attacker's /admin prepended to victim's request
```

### Smuggling Attack Scenarios

| Scenario | Attack | Impact |
|----------|--------|--------|
| Prefix | Smuggle high-privilege request before victim's | Privilege escalation |
| Desynchronization | Split request/response | Request hijacking |
| Cache bypass | Poison cache with smuggled request | Cache poisoning |
| WAF bypass | Hide malicious request in prefix | Bypass security controls |
| Session fixation | Smuggle session-setting request | Hijack user session |

## Cache Poisoning

### Mechanism

Cache poisoning exploits HTTP caching to serve attacker-controlled content to legitimate users.

### Attack Prerequisites

1. Application accepts and processes HTTP/2 headers
2. Caching layer (CDN, proxy, browser) uses certain headers in cache key
3. Headers can be injected with attacker values
4. Cache TTL allows long-lived poisoning

### Example 1: X-Forwarded-For Poisoning

```http
# Attacker sends:
GET /api/user/profile HTTP/2
Host: cdn.example.com
X-Forwarded-For: attacker.com

# Cache key (if using X-Forwarded-For):
  Key = "/api/user/profile" + "attacker.com"
  Value = attacker's profile page

# Victim sends (different X-Forwarded-For):
GET /api/user/profile HTTP/2
Host: cdn.example.com
X-Forwarded-For: victim.com

# Cache key:
  Key = "/api/user/profile" + "victim.com"
  # Different key, different response (not poisoned in this case)

# BUT if cache uses only path:
  Key = "/api/user/profile"
  # All users get attacker's response!
```

### Example 2: Host Header Poisoning

```http
# Attacker sends:
GET / HTTP/2
Host: attacker.com  # Injected via HTTP/2 header confusion

# Legitimate request:
GET / HTTP/2
Host: example.com

# If cache key doesn't include Host:
  Both map to same cache entry
  Attacker's response returned for example.com
```

### Example 3: Connection-Specific Header Poisoning

```http
# Vulnerable cache considers these in key:
GET /resource HTTP/2
Connection: close          # Injected
Content-Type: text/plain

# Attacker creates cache entry for this specific combination
# Later victim with different Connection header gets fresh version

# But more dangerously:
GET /resource HTTP/2
Connection: upgrade\r\nSet-Cookie: admin=true

# If cache ignores Connection header but processes Set-Cookie:
  Injected cookie served to all users
```

### Cache Poisoning Impact

- **Malware Distribution:** Serve malware instead of legitimate software
- **Credential Theft:** Replace login form with phishing form  
- **XSS:** Inject JavaScript into cached pages
- **SEO Poisoning:** Inject malicious links
- **Ad Injection:** Inject attacker's ads (revenue theft)

## Protocol Confusion

### Mechanism

Protocol confusion occurs when different layers interpret protocol differently, causing security bypasses.

### Example 1: HTTP/2 to HTTP/1.1 Downgrade

```http
# Attacker sends in HTTP/2:
Upgrade: h2c

# HTTP/2 implementation: Ignores (already HTTP/2)
# Vulnerable proxy/backend: Attempts downgrade to HTTP/1.1
# Attacker then uses HTTP/1.1 smuggling attacks
```

### Example 2: Transfer-Encoding Confusion

```
# HTTP/2 perspective:
Frame 1: HEADERS
  Transfer-Encoding: chunked
  Content-Length: 50

Frame 2: DATA (100 bytes) <- Frame determines actual message size

# HTTP/1.1 backend perspective (if forwarded):
Transfer-Encoding: chunked <- Process as chunked
Content-Length: 50 <- Also present

# Different interpretation of message boundary
```

### Example 3: Trailer Confusion

```http
# HTTP/2:
HEADERS frame: Trailer: X-Signature
DATA frames: [body content]
CONTINUATION frame: X-Signature: [value]

# HTTP/1.1 interpretation (if translated incorrectly):
Trailer: X-Signature
[body data]
X-Signature: value

# Different handling of trailers = confusion
# Security-critical trailers (signatures) might be misplaced
```

### Protocol Confusion Impact

- **Authentication Bypass:** Skip authentication layer
- **Privilege Escalation:** Hide authorization checks
- **Security Filter Bypass:** Bypass WAF/IDS
- **Response Manipulation:** Attacker-controlled responses

## Exploitation Chains

### Complete Attack Chain 1: Cache Poisoning via Response Splitting

```
1. Reconnaissance
   - Identify HTTP/2 endpoint
   - Identify caching layer (CDN, proxy)
   - Identify cache key components

2. Crafting Payload
   - Inject header with CRLF: \r\n\r\n[malicious response]
   - Craft response to appear legitimate

3. Injection
   - Send crafted request with injected header
   - Caching layer accepts and caches response

4. Exploitation
   - Legitimate users request same resource
   - Receive attacker's cached malicious response
   - Example: Receive malicious HTML instead of JSON
```

### Complete Attack Chain 2: Request Smuggling to Admin Access

```
1. Reconnaissance
   - Identify proxy → backend architecture
   - Identify admin endpoints
   - Identify how Transfer-Encoding is handled

2. Crafting Payload
   - Create message with Transfer-Encoding causing smuggling
   - Prefix: attacker's admin request
   - Main: legitimate user's request

3. Injection
   - Send via HTTP/2 to proxy
   - Proxy validates, forwards to HTTP/1.1 backend

4. Backend Desynchronization
   - Backend splits messages at different boundary
   - Attacker's request executes as if from legitimate user's session

5. Exploitation
   - Gain admin access via smuggled request
   - Persistent access if session captured
```

## Detection and Defense

### Detection Indicators

#### Log Patterns to Monitor

```
# Header injection attempts:
- Multiple Transfer-Encoding headers
- Transfer-Encoding with \r\n patterns
- Whitespace in Transfer-Encoding value
- CRLF sequences in header values

# Response splitting indicators:
- Double CRLF (\r\n\r\n) in user input
- Injected HTTP responses in logs
- Multiple responses from single request

# Request smuggling:
- Mismatched Content-Length and Transfer-Encoding
- Different message boundaries detected
- Chunked encoding with content-length

# Suspicious headers:
- Transfer-Encoding in HTTP/2 request
- Connection header in HTTP/2 request
- Keep-Alive in HTTP/2 request
- Upgrade in multiplexed stream
```

#### Monitoring Queries

```sql
-- Find requests with forbidden headers
SELECT * FROM http_logs 
WHERE protocol = 'HTTP/2' 
AND (
  header_name IN ('transfer-encoding', 'connection', 'keep-alive', 'upgrade', 'proxy-connection', 'trailer')
);

-- Find potential injection attempts
SELECT * FROM http_logs 
WHERE header_value LIKE '%\r\n%'
OR header_value LIKE '%\n%';

-- Find protocol confusion attempts
SELECT * FROM http_logs 
WHERE protocol = 'HTTP/2' 
AND (
  header_name = 'upgrade' 
  OR (header_name = 'connection' AND header_value = 'upgrade')
);
```

### Defense Mechanisms

#### 1. Input Validation

```python
def validate_http2_headers(headers):
    forbidden = {'transfer-encoding', 'connection', 'keep-alive', 'upgrade', 'proxy-connection', 'trailer'}
    
    for name, value in headers.items():
        # Check header name
        if name.lower() in forbidden:
            raise HeaderValidationError(f"Forbidden header: {name}")
        
        # Check for CRLF in value
        if '\r' in value or '\n' in value:
            raise HeaderValidationError(f"Invalid characters in header: {name}")
        
        # Check header length
        if len(name) > 8192 or len(value) > 8192:
            raise HeaderValidationError(f"Header exceeds size limit: {name}")
    
    return True
```

#### 2. Early Rejection

Reject at the earliest point possible:
- Before request processing
- Before header forwarding
- Before response generation
- Before caching

#### 3. Protocol Enforcement

```python
def enforce_http2_protocol(request):
    if request.protocol == 'HTTP/2':
        # HTTP/2 specific validation
        forbidden_headers = {'transfer-encoding', 'connection', 'keep-alive', 'upgrade', 'proxy-connection', 'trailer'}
        
        for header in request.headers:
            if header.lower() in forbidden_headers:
                return HTTP400_BAD_REQUEST
        
        # Additional HTTP/2 validations
        # ...
    
    return None  # OK
```

#### 4. Header Normalization

```python
def normalize_headers(headers):
    normalized = {}
    
    for name, value in headers.items():
        # Remove leading/trailing whitespace
        name = name.strip()
        value = value.strip()
        
        # Reject if contains CRLF
        if '\r' in value or '\n' in value:
            raise ValidationError("Invalid header value")
        
        # Normalize header name (lowercase)
        normalized[name.lower()] = value
    
    return normalized
```

#### 5. Configuration Best Practices

```yaml
# nginx configuration
server {
    listen 80 http2;
    
    # Reject requests with forbidden headers
    if ($http_transfer_encoding) {
        return 400;
    }
    
    if ($http_connection) {
        return 400;
    }
    
    if ($http_keep_alive) {
        return 400;
    }
    
    if ($http_upgrade) {
        return 400;
    }
    
    # Add security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

### Testing Strategies

#### Automated Testing

```bash
# Test each forbidden header
for header in "Transfer-Encoding: chunked" \
              "Connection: close" \
              "Keep-Alive: timeout=5" \
              "Upgrade: h2c" \
              "Proxy-Connection: keep-alive" \
              "Trailer: X-Signature"
do
  echo "Testing: $header"
  curl -H "$header" http://localhost:8000/api/test
done
```

#### Manual Testing

1. Use Burp Suite Repeater
2. Manually craft requests with forbidden headers
3. Observe rejection/acceptance
4. Try injection and splitting payloads
5. Monitor logs for alerts

#### Fuzzing

```python
# Fuzzing framework
forbidden_headers = ['Transfer-Encoding', 'Connection', 'Keep-Alive', 'Upgrade', 'Proxy-Connection', 'Trailer']
injection_patterns = ['value\r\nX-Injected: malicious', 'value\r\n\r\n<response>']

for header in forbidden_headers:
    for pattern in injection_patterns:
        payload = f"{header}: {pattern}"
        response = send_request(payload)
        assert response.status == 400, f"Failed for {header}: {pattern}"
```

## Exploitation Tools

### curl

```bash
curl -H "Transfer-Encoding: chunked" http://localhost:8000/api/test
curl -v --http2 -H "Connection: close" http://localhost:8000/api/test
```

### Burp Suite

1. Proxy → Intercept
2. Intercept request
3. Modify headers → Add forbidden header
4. Forward or Send to Repeater

### Custom Scripts

```python
import requests

# Test endpoint
url = "http://localhost:8000/api/test"

# Forbidden headers to test
headers_to_test = [
    {"Transfer-Encoding": "chunked"},
    {"Connection": "close"},
    {"Keep-Alive": "timeout=5"},
    {"Upgrade": "h2c"},
]

for headers in headers_to_test:
    response = requests.post(url, headers=headers)
    print(f"Headers: {headers} → Status: {response.status_code}")
```

### Remediation Verification

After fixing the vulnerability:

```python
def test_http2_header_validation():
    """Verify ASVS 4.2.3 compliance"""
    
    forbidden_headers = ['transfer-encoding', 'connection', 'keep-alive', 'upgrade', 'proxy-connection', 'trailer']
    
    for header in forbidden_headers:
        response = client.post(
            '/api/test',
            headers={header: 'value'},
            environ_base={'SERVER_PROTOCOL': 'HTTP/2'}
        )
        assert response.status_code == 400, f"Should reject {header}"
    
    # Valid request should pass
    response = client.post('/api/test', environ_base={'SERVER_PROTOCOL': 'HTTP/2'})
    assert response.status_code == 200

print("ASVS 4.2.3 validation tests passed!")
```

## Conclusion

ASVS 4.2.3 addresses critical vulnerabilities in HTTP/2 implementations:

- **Header Injection:** Inject arbitrary headers
- **Response Splitting:** Inject complete responses
- **Request Smuggling:** Confuse message boundaries
- **Cache Poisoning:** Serve malicious content
- **Protocol Confusion:** Exploit layer misunderstandings

**Proper implementation requires:**
1. Early validation of forbidden headers
2. Protocol-aware security controls
3. Comprehensive testing
4. Continuous monitoring
5. Defense-in-depth approach

Never trust user input, even in headers. Always validate early, validate often.
