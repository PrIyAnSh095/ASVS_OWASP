# ASVS 4.2.4 — Attack Document: CRLF Injection

## Overview

This document provides detailed attack scenarios for CRLF injection vulnerabilities relevant to ASVS 4.2.4. All examples are for educational use in the lab environment only.

---

## Attack 1: Header Injection

### Description

Header injection occurs when user-controlled data containing `\r\n` is placed directly into an HTTP response header value without validation. The injected newline terminates the current header and begins a new one.

### Vulnerable Code Pattern

```python
# VULNERABLE — user input reflected directly in response header
@app.route("/api/echo-header")
def echo_header():
    user_value = request.args.get("value", "")
    resp = make_response(jsonify({"ok": True}))
    resp.headers["X-Echo"] = user_value   # ← INJECTION POINT
    return resp
```

### Attack Payload

```
GET /api/echo-header?value=legitimate%0d%0aSet-Cookie:%20session=attacker HTTP/1.1
Host: target.com
```

URL-decoded `value`:
```
legitimate\r\nSet-Cookie: session=attacker
```

### Resulting HTTP/1.1 Response (before fix)

```
HTTP/1.1 200 OK\r\n
Content-Type: application/json\r\n
X-Echo: legitimate\r\n
Set-Cookie: session=attacker\r\n         ← INJECTED
\r\n
{"ok": true}
```

### Impact

The browser receives a response with an attacker-controlled `Set-Cookie` header, potentially overwriting the victim's session cookie.

### Prevention (ASVS 4.2.4)

```python
import re
CRLF_PATTERN = re.compile(r"[\r\n]")

@app.route("/api/echo-header")
def echo_header():
    user_value = request.args.get("value", "")
    if CRLF_PATTERN.search(user_value):
        return jsonify({"error": "Invalid header value"}), 400
    resp = make_response(jsonify({"ok": True}))
    resp.headers["X-Echo"] = user_value
    return resp
```

---

## Attack 2: HTTP Response Splitting

### Description

Response splitting uses a double CRLF (`\r\n\r\n`) to terminate the headers section entirely, injecting a complete second HTTP response. This is an escalation of header injection.

### Attack Payload

```
value%0d%0a%0d%0aHTTP%2F1.1%20200%20OK%0d%0aContent-Type%3A%20text%2Fhtml%0d%0a%0d%0a%3Chtml%3EInjected%3C%2Fhtml%3E
```

URL-decoded:
```
value\r\n\r\nHTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html>Injected</html>
```

### Resulting Raw Response

```
HTTP/1.1 200 OK\r\n
Content-Type: application/json\r\n
X-Custom: value\r\n
\r\n                                    ← Attacker ends response 1 headers
HTTP/1.1 200 OK\r\n                     ← Attacker starts response 2
Content-Type: text/html\r\n
\r\n
<html>Injected</html>                   ← Attacker's body
```

### Cache Poisoning via Response Splitting

If a shared cache (Varnish, Nginx proxy cache, CDN) is between the client and server:

1. Attacker sends the response-splitting request to a cacheable endpoint
2. Cache receives and splits the "two responses"
3. Cache associates the second response with the next URL in the pipeline
4. All users requesting that URL receive the attacker's injected response

### Impact

- **Mass XSS**: If injected response contains `<script>`, all users are XSS'd
- **Credential Theft**: `Set-Cookie` in injected response for all users
- **Defacement**: Replace cached page content

---

## Attack 3: Log Injection

### Description

When server logs record HTTP header values without sanitization, an attacker can inject `\n` to create fake log entries. This is particularly dangerous for:
- Security incident analysis
- SIEM/SOC monitoring
- Audit trails
- Compliance logging

### Vulnerable Code Pattern

```python
# VULNERABLE — unsanitized value logged directly
logger.info("Request from %s with header X-User-Id: %s", ip, user_id_header)
```

### Attack Payload

Attacker sends:
```
X-User-Id: alice
            \n2024-07-03 [INFO] ADMIN authentication SUCCESS user=administrator ip=192.168.1.100
```

### Resulting Log File

```
2024-07-03 14:00:00 [INFO] Request from 10.0.0.5 with header X-User-Id: alice
2024-07-03 14:00:00 [INFO] ADMIN authentication SUCCESS user=administrator ip=192.168.1.100
```

The second line is entirely fabricated. A security analyst reviewing the log would see a false admin authentication event.

### Consequences

1. **Evidence Tampering**: Attacker hides their own malicious entries by flooding logs with noise
2. **False Positives**: Triggers security alerts for non-existent events, wasting analyst time
3. **Framing**: Frames innocent users (e.g., `user=alice IP=8.8.8.8`)
4. **Log Parser Injection**: If logs are parsed by SIEM rules expecting specific formats, injected content can break parsing or trigger false SIEM rules

### Prevention

```python
import re

def sanitize_for_log(value: str) -> str:
    """Remove CR/LF from strings before logging."""
    return re.sub(r"[\r\n]", " [NEWLINE] ", value)

logger.info("Request with header: %s", sanitize_for_log(user_value))
```

---

## Attack 4: Cache Poisoning via CRLF

### Description

Cache Poisoning combines response splitting with the presence of a caching intermediary. The attacker's goal is to have the cache store and serve a malicious response to legitimate users.

### Attack Flow

```
Attacker                     Cache                    Origin Server
   |                           |                           |
   |---[CRLF request]--------->|                           |
   |                           |---[Forward request]------>|
   |                           |<--[Split response]--------|
   |<--[Response 1 headers]----|                           |
   |                           |                           |
   |--- [Next request] ------->|                           |
   |<-- [Attacker's cached     |                           |
   |     poisoned response] ---|                           |
```

### Real-World Context

This attack is most effective against:
- **CDNs**: Cloudflare, Fastly, Akamai
- **Reverse proxies**: Varnish, Nginx proxy
- **Application caches**: Redis-backed response caches

### Example: Open Redirect + Cache Poisoning

```
# Application has an open redirect:
GET /go?url=https://safe-site.com HTTP/1.1

# Attacker crafts:
GET /go?url=https://safe-site.com%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0a%0d%0a<script>steal()</script>
```

The cache stores `<script>steal()</script>` as the body for `/go?url=https://safe-site.com`. All subsequent visitors to this URL receive the malicious script.

---

## Attack 5: Email Header Injection (Related Concept)

Although not directly related to HTTP, the same CRLF injection principle applies to email headers (SMTP uses CRLF termination):

```
# Vulnerable mail form:
mail_headers = f"To: {user_email}\r\nSubject: {subject}"

# Attack input for email:
subject = "Hello\r\nBcc: attacker@evil.com\r\nCc: victim2@corp.com"
```

This injects additional SMTP headers, enabling spam and phishing at scale.

---

## Common Developer Mistakes

### Mistake 1: Assuming URL Encoding Prevents Injection

```python
# WRONG ASSUMPTION: %0d%0a won't cause injection
user_val = urllib.parse.unquote(request.args.get("val", ""))
resp.headers["X-Val"] = user_val  # URL-decoded value may contain \r\n
```

**Fix**: Validate AFTER decoding.

### Mistake 2: Trusting Framework to Strip CRLF

```python
# WRONG: Assuming Flask/Werkzeug strips \r\n from all header values
# Flask may block it at HTTP/2 frame level but NOT in JSON body processing
resp.headers["X-Val"] = json_body["value"]  # JSON value may contain \r\n
```

**Fix**: Validate user-controlled values before using them as header values, regardless of source.

### Mistake 3: Sanitizing Only in Output, Not Input

Some developers try to strip CRLF when setting headers but miss validation at the request input stage. ASVS 4.2.4 requires rejecting requests, not just sanitizing output.

### Mistake 4: Only Checking the Value, Not the Name

```python
# INCOMPLETE — only checks value
if "\r" in header_value or "\n" in header_value:
    return 400

# Header name can also be injected:
# header_name = "X-Foo\r\nSet-Cookie: evil=1"
```

**Fix**: Check both header names AND values.

### Mistake 5: Using String Replacement Instead of Rejection

```python
# WRONG — sanitizes instead of rejects
clean_value = header_value.replace("\r", "").replace("\n", "")
resp.headers["X-Val"] = clean_value
```

ASVS 4.2.4 requires **rejection** of requests, not silent sanitization. Silent sanitization masks attacks and doesn't alert on malicious activity.
