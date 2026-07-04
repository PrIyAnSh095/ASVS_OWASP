# ASVS 4.2.4 — Theory: HTTP Headers, CRLF, and Injection Attacks

## 1. HTTP Header Structure

HTTP messages (requests and responses) consist of:

```
Start-Line\r\n
Header-Name: Header-Value\r\n
Header-Name: Header-Value\r\n
\r\n                          ← Empty line signals end of headers
Message-Body
```

Each header line is terminated by a **CRLF** sequence — Carriage Return (CR, `0x0d`) followed by Line Feed (LF, `0x0a`). The empty line separating headers from the body is also a CRLF.

### Header Field Syntax (RFC 7230 §3.2)

```
header-field = field-name ":" OWS field-value OWS
field-name   = token
field-value  = *( field-content / obs-fold )
field-content = field-vchar [1*( SP / HTAB ) field-vchar]
field-vchar  = VCHAR / obs-text
```

Critically, `field-value` **must not** contain CR or LF characters except as part of the CRLF separator between headers.

## 2. What is CR, LF, and CRLF?

### CR — Carriage Return

| Property | Value |
|----------|-------|
| Character | `\r` |
| ASCII code | 13 (decimal) |
| Hex | `0x0d` |
| Origin | Teletype machine: returns print head to start of line |
| HTTP role | First byte of header-line terminator |

### LF — Line Feed

| Property | Value |
|----------|-------|
| Character | `\n` |
| ASCII code | 10 (decimal) |
| Hex | `0x0a` |
| Origin | Advances paper to next line |
| HTTP role | Second byte of header-line terminator |

### CRLF — Carriage Return + Line Feed

In HTTP/1.1, every header line ends with `\r\n`. The header section ends with a blank line: `\r\n\r\n`.

```
HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n
Set-Cookie: session=abc123\r\n
\r\n
<html>Body here</html>
```

## 3. What is CRLF Injection?

**CRLF injection** occurs when an attacker embeds `\r`, `\n`, or `\r\n` characters into user-controlled input that is subsequently used in an HTTP message without validation.

### Why It's Dangerous

If an application takes user input and places it directly into an HTTP header value:

```python
# VULNERABLE — no validation
response.headers["X-Custom"] = user_supplied_value
```

And the user supplies:
```
legitimate-value\r\nSet-Cookie: session=attacker
```

The raw HTTP/1.1 response bytes become:
```
HTTP/1.1 200 OK\r\n
Content-Type: application/json\r\n
X-Custom: legitimate-value\r\n            ← Attacker ends the X-Custom header here
Set-Cookie: session=attacker\r\n          ← Attacker injects a new header
\r\n
{"status": "ok"}
```

The parser (browser, proxy, curl) reads this as a response with an additional `Set-Cookie` header — one the attacker injected.

## 4. Header Injection

**Header Injection** (CWE-644) occurs when an attacker injects arbitrary headers into an HTTP response by embedding `\r\n` into a header value.

### Attack Scenario

1. Application has an endpoint: `GET /redirect?url=https://example.com`
2. It sets `Location: {url}` in the response
3. Attacker requests: `GET /redirect?url=https://evil.com%0d%0aSet-Cookie:%20hijacked=true`
4. URL-decoded: `Location: https://evil.com\r\nSet-Cookie: hijacked=true`
5. The response now contains an attacker-controlled `Set-Cookie` header

### Impact

- Session hijacking via forged `Set-Cookie`
- Cross-Site Scripting via injected `Content-Type: text/html`
- Authentication bypass via injected `WWW-Authenticate` or `Authorization` headers
- Phishing via `Location` redirect manipulation

## 5. HTTP Response Splitting

**Response Splitting** (CWE-113) is a more severe form of header injection where the attacker injects a double CRLF (`\r\n\r\n`) to terminate the headers section and inject a complete second HTTP response.

### Attack Scenario

Attacker supplies:
```
value\r\n\r\n<html><body>Malicious Page</body></html>
```

The raw response becomes:
```
HTTP/1.1 200 OK\r\n
Content-Type: application/json\r\n
X-Custom: value\r\n
\r\n                          ← End of first response headers
<html><body>Malicious Page</body></html>  ← INJECTED SECOND RESPONSE
```

### Impact

Intermediaries (reverse proxies, CDNs, shared caches) may interpret this as two responses:

1. First response: `200 OK` with the injected body
2. "Second response": entirely crafted by the attacker

If the cache stores the injected second response, **all users** requesting the same URL receive the malicious content. This is **Cache Poisoning**.

## 6. Log Injection

**Log Injection** (CWE-117) occurs when unsanitized user input containing newlines is written to server logs.

### Attack Scenario

Log statement:
```python
logger.info("Processing header: value=%s", user_value)
```

Attacker supplies:
```
Mozilla/5.0\n2024-01-01 [INFO] ADMIN LOGIN from 10.0.0.1 user=admin
```

Server log becomes:
```
2024-01-01 [INFO] Processing header: value=Mozilla/5.0
2024-01-01 [INFO] ADMIN LOGIN from 10.0.0.1 user=admin   ← FAKE LOG ENTRY
```

### Impact

- Hide evidence of attacks by injecting noise
- Implicate innocent users by forging their log entries
- Confuse security monitoring and SIEM alerts
- Inject malicious content that triggers log parsing vulnerabilities

## 7. HTTP/2 Header Validation (RFC 9113)

HTTP/2 introduced binary framing, replacing HTTP/1.1's text-based message format.

### Binary Framing

In HTTP/2, headers are:
1. Compressed using HPACK (RFC 7541)
2. Transmitted as binary HEADERS frames
3. **Not** separated by CRLF sequences at the transport layer

### RFC 9113 §8.2.1 — Restrictions on Field Values

> "A field value MUST NOT contain characters in the ranges 0x00-0x08, 0x0a-0x1f, or 0x7f (i.e., all control characters other than HTAB (0x09))."

This explicitly forbids:
- LF (`0x0a`)
- CR (`0x0d`)

> "Endpoints MUST treat a message that contains a field value that violates any of these conditions as malformed. A request or response that is determined to be malformed MUST be treated as a stream error of type PROTOCOL_ERROR."

### What This Means in Practice

HTTP/2 servers reject malformed HEADERS frames at the protocol level. An attacker cannot inject raw `\r\n` bytes into HTTP/2 headers at the wire level — they would be rejected before reaching the application.

**However**: User-supplied data containing `\r\n` can still reach application code through:
- JSON request bodies
- URL query parameters (when URL-decoded)
- Form fields
- Request bodies processed by the application

ASVS 4.2.4 requires the **application** to validate this data before using it in any header context.

## 8. HTTP/3 Header Validation (RFC 9114)

HTTP/3 runs over QUIC (UDP) instead of TCP. It uses QPACK (RFC 9204) for header compression, replacing HPACK.

### RFC 9114 §4.2 — HTTP Fields

> "Characters in field values MUST NOT include the zero value (ASCII NUL, 0x00), line feed (0x0a), or carriage return (0x0d) at any position."

The same restrictions apply. HTTP/3 headers are transmitted in binary QPACK-encoded format, making raw CRLF injection at the transport level impossible.

The application-layer requirement remains identical to HTTP/2.

## 9. Why Is This Still Important?

Even though HTTP/2 and HTTP/3 prevent CRLF injection at the transport layer, ASVS 4.2.4 Level 3 requires application-level validation because:

### Reason 1: Downstream HTTP/1.1 Systems

Many architectures include HTTP/2 at the edge with HTTP/1.1 internally:

```
Client → [HTTP/2] → Reverse Proxy → [HTTP/1.1] → Application Server
```

If the reverse proxy forwards user-supplied headers to the application server over HTTP/1.1 without sanitization, CRLF injection becomes possible in the internal network.

### Reason 2: Log Injection

Application logs are text files. `\n` characters in logged header values create fake log entries regardless of the HTTP protocol version.

### Reason 3: Defence in Depth

ASVS Level 3 requires defence-in-depth security. Even if the transport layer provides some protection, the application must independently validate its inputs. If the transport layer is misconfigured, compromised, or bypassed, the application remains secure.

### Reason 4: Data Storage and Forwarding

Header values may be:
- Stored in databases (and retrieved later in HTTP/1.1 contexts)
- Forwarded to third-party APIs over HTTP/1.1
- Written to log files parsed by SIEM tools
- Used in email headers (which use CRLF termination)

## 10. Relevant RFCs

| RFC | Title | Relevant Section |
|-----|-------|-----------------|
| RFC 9113 | HTTP/2 | §8.2.1 — Field Validity |
| RFC 9114 | HTTP/3 | §4.2 — HTTP Fields |
| RFC 9204 | QPACK: Field Compression for HTTP/3 | General |
| RFC 7541 | HPACK: Header Compression for HTTP/2 | General |
| RFC 7230 | HTTP/1.1 Message Syntax and Routing | §3.2.6 — Field Value Components |
| RFC 7231 | HTTP/1.1 Semantics and Content | §3.1.1.5 — Content-Type |

## 11. Real-World Examples

### CVE-2019-18634 (sudo)
Although not HTTP, this illustrates the log injection principle: attacker-controlled input written to a privileged process's output.

### PHP Header Injection (Historical)
Prior to PHP 4.4.2 and 5.1.2, PHP's `header()` function accepted CRLF sequences, enabling response splitting via URL parameters in redirect pages.

### Apache Tomcat CRLF Injection (CVE-2016-6816)
Tomcat's `400 Bad Request` error page reflected unsanitized URL characters including `\r\n`, enabling header injection in the error response itself.

### Nginx Header Injection (Various)
Multiple Nginx configuration patterns that used `$request_uri` or other variables in `add_header` directives were vulnerable to CRLF injection when those variables contained URL-encoded `\r\n`.

### The Common Thread

In each case, user-controlled input containing `\r\n` reached a context where those characters had structural meaning (HTTP headers, log files) without validation. ASVS 4.2.4 directly addresses this class of vulnerability.
