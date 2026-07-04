# ASVS 4.2.3 Technical Theory

## Table of Contents

1. [HTTP Evolution](#http-evolution)
2. [HTTP/2 Architecture](#http2-architecture)
3. [Connection-Specific Headers](#connection-specific-headers)
4. [Why RFC 7540 Forbids These Headers](#why-rfc-7540-forbids-these-headers)
5. [Attack Vectors](#attack-vectors)
6. [Implementation Considerations](#implementation-considerations)
7. [Security Impact](#security-impact)

## HTTP Evolution

### HTTP/1.0 and HTTP/1.1

In HTTP/1.0 and HTTP/1.1, each HTTP request/response required:
- TCP connection establishment
- Single request/response pair
- Connection closure or reuse

**Connection Management Headers in HTTP/1.1:**
```
Connection: keep-alive       # Reuse this connection
Connection: close            # Close after response
Keep-Alive: timeout=5        # How long to keep alive
Upgrade: h2c                  # Suggest protocol upgrade
```

These headers were essential for performance optimization in HTTP/1.1.

### Limitations of HTTP/1.1

- **Head-of-Line Blocking:** One slow resource blocks everything behind it
- **Multiple Connections:** Browsers open 6-8 connections per domain (expensive)
- **Header Redundancy:** Same headers repeated for each connection
- **Inefficient:** Uncompressed headers, no prioritization

### HTTP/2 Solution

HTTP/2 addresses HTTP/1.1 limitations with:

1. **Binary Framing:** Switches from text to binary frames
2. **Multiplexing:** Multiple streams over one connection
3. **Header Compression:** HPACK compression reduces header overhead
4. **Server Push:** Send resources before requested
5. **Prioritization:** Indicate stream importance

## HTTP/2 Architecture

### Multiplexing Model

```
HTTP/1.1:
Connection 1: Request A ─────────────────────── Response A ──────
Connection 2: Request B ─────────────────────── Response B ──────
Connection 3: Request C ─────────────────────── Response C ──────

HTTP/2:
Stream 1: Request A ──── (frames) ──── Response A ──
Stream 3: Request B ──── (frames) ──── Response B ──────────
Stream 5: Request C ──── (frames) ──── Response C ────
└─ All over single TCP connection
```

### Key Concepts

**Connection:** Single TCP connection to a host
- Established once, reused for all requests
- Managed with GOAWAY frame (not Connection header)
- Persistent by design (no keep-alive needed)

**Stream:** Logical request/response sequence
- Identified by stream ID (odd for client-initiated, even for server-pushed)
- Independent flow control
- Can be prioritized

**Frame:** Smallest unit of HTTP/2 communication
- Frame type: DATA, HEADERS, PRIORITY, RST_STREAM, SETTINGS, PUSH_PROMISE, PING, GOAWAY, WINDOW_UPDATE, CONTINUATION
- All have explicit length field
- All contain stream ID

### Example HTTP/2 Stream

```
Frame 1: HEADERS (Stream 1)
  - Method: GET
  - Path: /index.html
  - Host: example.com
  - User-Agent: Chrome

Frame 2: DATA (Stream 1)
  - [empty, GET has no body]

Frame 3: HEADERS (Stream 1, response)
  - Status: 200
  - Content-Type: text/html

Frame 4: DATA (Stream 1)
  - [HTML content chunk 1]
  - [more chunks...]
```

## Connection-Specific Headers

### The Six Forbidden Headers

RFC 7540 Section 8.1.2 forbids these headers in HTTP/2:

#### 1. Transfer-Encoding

**HTTP/1.1 Purpose:**
```
Transfer-Encoding: chunked

# Tells recipient to expect:
# chunk_size\r\n
# chunk_data\r\n
# 0\r\n
# trailers\r\n
# \r\n
```

**Why Forbidden in HTTP/2:**
- HTTP/2 frames have explicit length fields
- Chunked encoding is internal to HTTP/2 (hidden from application)
- Presence indicates HTTP/1.1 confusion
- Could trigger parsing differences in proxies

**Attack Scenario:**
```
Attacker sends:
  Transfer-Encoding: chunked
  Content-Length: 100

HTTP/2 layer: Processes as single frame (uses frame length)
HTTP/1.1 backend: Interprets as chunked (processes differently)
Result: Request smuggling - attacker crafts message boundary confusion
```

#### 2. Connection

**HTTP/1.1 Purpose:**
```
Connection: keep-alive    # Keep connection alive
Connection: close         # Close after this response
Connection: Upgrade       # Suggest protocol upgrade
```

**Why Forbidden in HTTP/2:**
- HTTP/2 connections are managed with GOAWAY frame
- Connection is persistent by definition
- Multiple streams share connection (can't close for one stream)
- Indicates HTTP/1.1 confusion

**Attack Scenario:**
```
Attacker sends:
  Connection: close

If processed by HTTP/2 layer: Ignored
If forwarded to HTTP/1.1 backend: Closes entire connection
Result: Denial of service to other users sharing the connection
```

#### 3. Keep-Alive

**HTTP/1.1 Purpose:**
```
Keep-Alive: timeout=5, max=100

# Specifies:
# - How long to keep idle connection alive (5 seconds)
# - How many requests before closing (100 requests)
```

**Why Forbidden in HTTP/2:**
- HTTP/2 connections don't need keep-alive heartbeats
- Connection state maintained with SETTINGS frames
- Idle timeout is connection-level concept (not applicable to HTTP/2)
- Presence indicates HTTP/1.1 confusion

**Attack Scenario:**
```
Attacker sends:
  Keep-Alive: timeout=0

Vulnerable HTTP/2 proxy: Interprets as "close immediately"
Result: Forces connection closure, disrupting other streams
```

#### 4. Upgrade

**HTTP/1.1 Purpose:**
```
Upgrade: h2c           # Upgrade to HTTP/2 Cleartext
Upgrade: websocket     # Upgrade to WebSocket
```

**Why Forbidden in HTTP/2:**
- Already using HTTP/2 (upgrade already happened)
- Upgrade negotiation happens at connection setup, not per-stream
- Sending in HTTP/2 stream is meaningless
- Could trigger protocol downgrade attacks

**Attack Scenario:**
```
Attacker sends in HTTP/2 stream:
  Upgrade: h2c

Vulnerable implementation: Attempts upgrade to HTTP/2
Result: Protocol downgrade or parsing confusion
```

#### 5. Proxy-Connection

**HTTP/1.1 Purpose:**
```
Proxy-Connection: keep-alive  # Non-standard, similar to Connection
```

**Why Forbidden in HTTP/2:**
- Non-standard header (never standardized in RFC)
- Presence strongly indicates HTTP/1.1
- May confuse proxies and proxies may interpret incorrectly
- Subject to header injection attacks

#### 6. Trailer

**HTTP/1.1 Purpose:**
```
Trailer: X-Custom-Trailer, X-Signature

# Indicates trailers will follow chunked body:
# chunk1\r\n
# [data]\r\n
# chunk2\r\n
# [data]\r\n
# 0\r\n
# X-Custom-Trailer: value\r\n
# X-Signature: value\r\n
# \r\n
```

**Why Forbidden in HTTP/2:**
- HTTP/2 trailers are handled via CONTINUATION frames
- Trailer headers are still sent (via trailers mechanism)
- But explicit Trailer header field is not used
- Different handling than HTTP/1.1 could cause confusion

**Attack Scenario:**
```
Attacker sends in HTTP/2:
  Trailer: X-Authorization

Vulnerable app: Processes as HTTP/1.1 trailer
Backend: Expects trailer in body, not in frames
Result: Security header bypassed due to parsing confusion
```

## Why RFC 7540 Forbids These Headers

### Reason 1: Architectural Mismatch

HTTP/2 multiplexing makes connection-scoped concepts invalid:

| Concept | HTTP/1.1 | HTTP/2 |
|---------|----------|--------|
| Connection | One request per connection | Multiple streams per connection |
| Keep-Alive | Negotiated per connection | Always persistent |
| Upgrade | Per-connection negotiation | Done at connection start |
| Trailers | With chunked body | Via frame trailers |
| Transfer-Encoding | Header-level framing | Frame-level framing |

### Reason 2: Security

Connection-specific headers enable attacks:

1. **Header Injection:** CRLF in header values can inject new headers
2. **Response Splitting:** Response header injection enables full response injection
3. **Request Smuggling:** Different interpretation of message boundaries
4. **Protocol Confusion:** Inconsistent parsing between layers
5. **Cache Poisoning:** Injected headers used in cache keys

### Reason 3: Simplification

HTTP/2 was designed to remove HTTP/1.1 complications:

- No need for connection persistence negotiation
- No header fields for connection-specific features
- Cleaner protocol reduces implementation bugs
- Reduces attack surface

## Attack Vectors

### Attack 1: Header Injection

**Technique:**
```
User-Agent: curl
X-Injection: value\r\nX-Injected: malicious\r\n

# If interpreted as:
X-Injection: value
X-Injected: malicious
```

**Impact:**
- Inject arbitrary headers
- If reflected in response or forwarded to backend, enables attacks
- Can inject authentication headers, override security decisions

**Example:**
```
# Legitimate flow
GET /api/user HTTP/2
Authorization: Bearer token123

# Attacker attempts injection
GET /api/user HTTP/2
Authorization: Bearer token123
Transfer-Encoding: chunked\r\nAuthorization: Bearer attacker-token
```

### Attack 2: Response Splitting

**Technique:**
```
Host: example.com\r\n
\r\n
HTTP/1.1 302 Found
Location: http://attacker.com
\r\n
```

**Impact:**
- Inject entire HTTP response
- Attacker can make victim's browser load attacker's content
- Leads to phishing, XSS, etc.
- Works if application echoes unvalidated headers in response

### Attack 3: Request Smuggling

**Technique:**
```
POST /api/transfer HTTP/2
Transfer-Encoding: chunked
Content-Length: 50

# HTTP/2 layer: Uses frame length (ignores headers)
# HTTP/1.1 backend: Processes Transfer-Encoding, interprets differently
# Result: Message boundary confusion
```

**Example Attack:**
```
# Attacker's HTTP/2 request to proxy
POST /transfer HTTP/2
Transfer-Encoding: chunked
Content-Length: 200

# Proxy interprets with Content-Length from HTTP/1.1 header
# Backend interprets differently (uses chunking)
# Different boundaries = request smuggling
# Attacker's crafted end-to-start in attacker's payload, 
# can prepend to victim's next request

0\r\n
\r\n
GET /admin HTTP/1.1\r\nHost: localhost\r\n\r\n
```

### Attack 4: Cache Poisoning

**Technique:**
```
GET /users/profile HTTP/2
Host: example.com
Pragma: no-cache
X-Forward-For: attacker.com

# If cache uses headers for key:
# cache_key = Host + User-Agent + X-Forward-For
# 
# Attacker poisons cache with attacker.com
# Legitimate users get attacker-controlled response
```

### Attack 5: Protocol Confusion Downgrade

**Technique:**
```
GET /api HTTP/2
Upgrade: h2c
Connection: upgrade

# If vulnerable app processes upgrade:
# Might downgrade to HTTP/1.1
# Attacker then uses HTTP/1.1 request smuggling
```

## Implementation Considerations

### Secure Implementation Pattern

```python
FORBIDDEN_HTTP2_HEADERS = {
    'transfer-encoding',
    'connection',
    'keep-alive',
    'upgrade',
    'proxy-connection',
    'trailer'
}

def validate_http2_request(request):
    """Reject if contains forbidden headers"""
    if is_http2_request(request):
        for header in request.headers:
            if header.lower() in FORBIDDEN_HTTP2_HEADERS:
                return 400, "Forbidden header in HTTP/2"
    return None, None
```

### Key Validation Points

1. **Protocol Detection:** How to identify HTTP/2?
   - Check `SERVER_PROTOCOL` environment variable
   - Check `h2` in connection info
   - Application parameter (for testing)

2. **Timing:** When to validate?
   - Before processing any request
   - Early in request pipeline
   - Cannot process and then reject (defense-in-depth)

3. **Response:** How to reject?
   - HTTP 400 Bad Request
   - Include explanation in response
   - Log incident for security monitoring

4. **Edge Cases:**
   - Case-insensitive header names
   - HTTP/1.1 compatibility mode
   - Proxy handling of headers

### Testing Strategy

1. **Unit Tests:** Test decorator/validator with each header
2. **Integration Tests:** Test with actual HTTP/2 client
3. **Protocol Tests:** Test with proxy, backends, CDN
4. **Security Tests:** Attempt injections, smuggling, splitting
5. **Performance Tests:** Ensure validation doesn't impact performance

## Security Impact

### CVSS Score

Vulnerability without this control:

- **Vector:** CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- **Score:** 9.8 (CRITICAL)

**Reasoning:**
- **AV:N** - Network accessible
- **AC:L** - Low complexity (send headers)
- **PR:N** - No privileges required (public API)
- **UI:N** - No user interaction needed
- **C:H, I:H, A:H** - Can compromise confidentiality, integrity, availability

### Real-World Impact

1. **Data Breach:** Inject headers to bypass authentication
2. **Cache Poisoning:** Serve attacker content to all users
3. **XSS:** Inject response content via response splitting
4. **DoS:** Confuse proxies/backends causing service disruption
5. **Phishing:** Serve attacker page to legitimate users

### Compliance

- **ASVS Level 3:** Required for comprehensive security
- **OWASP Top 10:** Related to injection attacks (A03:2021)
- **PCI DSS 6.5.1:** Injection attack prevention
- **Common Requirements:** RFC 7540 compliance

## Practical Implications

### For Developers

1. Use framework HTTP/2 support (not custom implementation)
2. Validate headers early and often
3. Use standard validation libraries
4. Test with multiple HTTP/2 clients
5. Monitor logs for injection attempts

### For DevOps/Infrastructure

1. Use HTTP/2-capable reverse proxy (Nginx, HAProxy)
2. Configure proxy to validate headers
3. Monitor for protocol confusion attacks
4. Ensure all layers understand HTTP/2
5. Test compatibility with various clients

### For Security Teams

1. Include HTTP/2 header validation in code review
2. Test for this vulnerability in assessments
3. Monitor logs for suspicious headers
4. Educate developers on HTTP/2 security
5. Include in security training

## References

- [RFC 7540 - HTTP/2 Specification](https://tools.ietf.org/html/rfc7540)
- [RFC 7540 Section 8.1.2 - Connection-Specific Headers](https://tools.ietf.org/html/rfc7540#section-8.1.2)
- [RFC 7231 - HTTP/1.1 Semantics](https://tools.ietf.org/html/rfc7231)
- [HPACK - HTTP Header Compression](https://tools.ietf.org/html/rfc7541)
- [HTTP/2 Security Considerations](https://tools.ietf.org/html/rfc7540#section-10)
- [CWE-444: Inconsistent Interpretation](https://cwe.mitre.org/data/definitions/444.html)

## Conclusion

HTTP/2's multiplexing architecture fundamentally changed HTTP. Connection-specific headers are not just obsolete in HTTP/2 – they're actively dangerous. Accepting them enables:

- Header injection attacks
- Response splitting
- Request smuggling
- Cache poisoning
- Protocol confusion

**ASVS 4.2.3 requires rejecting these headers to maintain protocol integrity and security.**

Proper implementation involves:
1. Detecting HTTP/2 requests
2. Validating absence of forbidden headers
3. Early rejection with appropriate error response
4. Comprehensive testing and monitoring

This control is essential for modern web application security.
