# ASVS 4.2.4 — Solution Guide

> ⚠️ **Instructor Note**: This document contains the complete solution for all student challenges. Provide to students only after they have completed their own attempts.

---

## Challenge Solutions

### Challenge 1: CR Injection

**Task**: Submit a CR (`\r`) in a header value and observe the secure app's response.

**Solution**:

1. Open the secure app at http://localhost:5000
2. Click the **CR Injection** preset button
3. The header value field will contain: `value\rSet-Cookie: evil=1` (with a real CR character)
4. Click **Test Header**

**Expected Result**:
- HTTP 400 Bad Request
- `"verdict": "REJECTED"`
- Violation: `"Header 'X-Attack-Header' value '...' contains CR/LF sequence"`
- `"asvs_pass": true`

**Explanation**: The `CRLF_PATTERN = re.compile(r"[\r\n]")` regex matches `\r` (0x0d), triggering the rejection.

---

### Challenge 2: LF Injection

**Task**: Submit an LF (`\n`) in a header value. Compare with vulnerable app.

**Secure App Solution**:
- Same as Challenge 1 using the **LF Injection** preset
- HTTP 400, REJECTED

**Vulnerable App Solution**:
1. Open http://localhost:5001
2. Click **LF Injection** preset
3. Click **Inject Header**
4. Result: HTTP 200, `"verdict": "ACCEPTED"`, `"asvs_pass": false`
5. Examine the `simulated_http1_injection` field in the response

**Comparison**:

| App | HTTP Status | Verdict | ASVS 4.2.4 |
|-----|------------|---------|-----------|
| Secure (5000) | 400 | REJECTED | ✅ PASS |
| Vulnerable (5001) | 200 | ACCEPTED | ❌ FAIL |

---

### Challenge 3: CRLF Injection

**Task**: Submit `\r\n` in a header value. Observe the violation detail.

**Solution**:

1. Use the **CRLF Injection** preset on either app
2. On the secure app, the rejection response includes:
   ```json
   {
     "violations": [
       "Header 'X-Attack-Header' value 'value\\r\\nSet-Cookie: session=hijacked' contains CR/LF sequence"
     ]
   }
   ```
3. The `repr()` of the value shows `\r\n` explicitly

**Key Insight**: A single regex `[\r\n]` catches CR, LF, and CRLF because `\r\n` contains both `\r` and `\n`.

---

### Challenge 4: Response Splitting

**Task**: Use the Response Split preset. Explain what would happen at an HTTP/1.1 downstream server.

**Solution**:

The **Response Split** preset sends:
```
value\r\n\r\n<html><body>Injected Page</body></html>
```

The double `\r\n\r\n` sequence terminates the HTTP response headers section. If this value reached an HTTP/1.1 application server:

**Request**:
```
POST /api/validate-header HTTP/1.1
Content-Type: application/json
{"header_name": "X-Attack", "header_value": "value\r\n\r\n<html>Injected</html>"}
```

**What the server would write as the HTTP/1.1 response**:
```
HTTP/1.1 200 OK\r\n
Content-Type: application/json\r\n
X-Attack: value\r\n
\r\n                       ← End of headers
<html>Injected</html>      ← Attacker's body parsed as the response body
```

Any caching intermediary would store `<html>Injected</html>` as the response body. All subsequent users requesting the same URL would receive the attacker's content.

---

### Challenge 5: Fix the Vulnerable App

**Task**: Add CRLF validation to `vulnerable/app.py` to make it ASVS 4.2.4 compliant.

**Complete Solution**:

Add at the top of `vulnerable/app.py` (after imports):

```python
import re

CRLF_PATTERN = re.compile(r"[\r\n]")

def validate_headers(headers: dict) -> list[str]:
    """
    Inspect every header name and value for CR/LF sequences.
    Returns a list of violation strings.
    """
    violations = []
    for name, value in headers.items():
        if CRLF_PATTERN.search(name):
            violations.append(f"Header name '{repr(name)}' contains CR/LF sequence")
        if CRLF_PATTERN.search(value):
            violations.append(f"Header '{name}' value '{repr(value[:80])}' contains CR/LF sequence")
    return violations
```

Add after the Flask app initialization:

```python
@app.before_request
def enforce_no_crlf_in_headers():
    """
    ADDED: Global CRLF validation hook.
    This makes the app compliant with ASVS 4.2.4.
    """
    violations = validate_headers(dict(request.headers))
    if violations:
        return jsonify({
            "status": "REJECTED",
            "asvs_control": "4.2.4",
            "violations": violations,
        }), 400
```

Also update `api_validate_header()` to add validation before processing:

```python
@app.route("/api/validate-header", methods=["POST"])
def api_validate_header():
    data = request.get_json(force=True, silent=True) or {}
    header_name = str(data.get("header_name", "X-Test-Header"))
    header_value = str(data.get("header_value", ""))

    # FIX: Add CRLF validation
    violations = validate_headers({header_name: header_value})
    if violations:
        return jsonify({
            "verdict": "REJECTED",
            "asvs_pass": True,
            "violations": violations,
        }), 400

    # ... rest of function
```

**Verification**: After making these changes, restart the Docker container and test with the CRLF payloads. All injection attempts should now return HTTP 400.

---

### Challenge 6: Framework Limits

**Task**: Try sending raw CRLF via curl. Explain why curl/h2 prevents it.

**Expected curl Error**:
```bash
$ curl -H "X-Attack: value\r\nSet-Cookie: evil=1" http://localhost:5001/
curl: option -H: headers must not contain embedded carriage returns or linefeeds
```

**Explanation**:

curl enforces RFC 7230 §3.2.6 which states: "No whitespace is allowed between the header field-name and colon. [...] field-value [...] MUST NOT contain a CR or LF."

HTTP/2 additionally prevents it at the wire level via HPACK binary encoding (RFC 9113 §8.2.1).

**Why This Is Not Sufficient**:

```
User Input → [curl/browser HTTP client]
                    ↓
              HTTP/2 framing ← Blocks raw CRLF in headers
                    ↓
              Application receives request
                    ↓
              JSON body parsing ← \r\n passes through as string
                    ↓
              Application code sets response header ← ATTACK POINT
                    ↓
              HTTP/1.1 backend or log file ← Vulnerable
```

The application must validate at the point where user-controlled data is used in header-setting code, log calls, or forwarded to downstream systems.

---

### Challenge 7: RFC Research

**Task**: Read RFC 9113 §8.2.1 and explain why HTTP/2 binary framing is not sufficient alone.

**Model Answer**:

RFC 9113 §8.2.1 states:

> "A field value MUST NOT contain characters in the ranges 0x00-0x08, 0x0a-0x1f, or 0x7f (i.e., all control characters other than HTAB (0x09)). Endpoints MUST treat a message that contains a field value that violates any of these conditions as malformed."

This means HTTP/2 servers must reject HEADERS frames containing LF (0x0a) or CR (0x0d). **This protection exists at the transport layer.**

**Why it's not sufficient alone**:

1. **Downstream HTTP/1.1**: Many microservice architectures use HTTP/2 externally and HTTP/1.1 internally. A malicious JSON body value containing `\r\n` passes through the HTTP/2 frame (as a string in JSON) and can be reflected in an HTTP/1.1 internal response.

2. **Log files are not HTTP/2**: Log files are plain text. `\n` in a logged header value creates a new log line regardless of transport protocol.

3. **Database persistence**: If the application stores user-supplied header values in a database and later retrieves them to set in responses, the HTTP/2 protection at receipt time does not protect the set-at-retrieval time.

4. **Defence in Depth (ASVS Level 3)**: Level 3 requires multiple independent layers of protection. Application code must not rely on infrastructure-level protections.

5. **RFC 9113 itself acknowledges this**: The RFC says endpoints "MUST treat" violations as errors, but this applies to the HTTP/2 endpoint. A Flask application receiving a POST body is not applying RFC 9113 to that body — it's simply processing a string.

**Conclusion**: ASVS 4.2.4 Level 3 requires the application to independently validate header values because:
- The transport layer protection only applies to the HTTP transport protocol itself
- It does not extend to application-layer data processing
- Multiple downstream sinks (logs, databases, HTTP/1.1 backends) are vulnerable to `\r\n` in string data
