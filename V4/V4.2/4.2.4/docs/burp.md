# ASVS 4.2.4 — Burp Suite Testing Walkthrough

## Overview

This guide explains how to use Burp Suite Community or Professional Edition to test ASVS 4.2.4 compliance. Because this lab uses HTTP/2 via Hypercorn, there are important nuances to understand about where and how CRLF injection can be demonstrated.

---

## Prerequisites

- Burp Suite Community or Professional Edition (v2023+)
- Docker containers running:
  - Secure app: http://localhost:5000
  - Vulnerable app: http://localhost:5001
- Browser configured to use Burp proxy (127.0.0.1:8080)

---

## Part 1: Configuring Burp for localhost

### Step 1: Browser Proxy Setup

1. In Burp, go to **Proxy → Proxy Settings**
2. Confirm the proxy listener is on `127.0.0.1:8080`
3. Configure your browser to use `127.0.0.1:8080` as HTTP/HTTPS proxy
4. For Firefox: Preferences → Network Settings → Manual Proxy → HTTP: `127.0.0.1`, Port `8080`

### Step 2: Intercept Verification

1. Turn Intercept ON in Burp's Proxy tab
2. Browse to `http://localhost:5000` in your browser
3. Confirm Burp captures the request
4. Turn Intercept OFF (we'll use Repeater for testing)

---

## Part 2: Capturing the Validation API Request

### Step 1: Browse to the Lab

Navigate to `http://localhost:5000` (secure) or `http://localhost:5001` (vulnerable).

### Step 2: Submit a Test Header

1. In the interactive lab UI, enter:
   - Header Name: `X-Test-Header`
   - Header Value: `legitimate-value`
2. Click **Test Header** (secure) or **Inject Header** (vulnerable)

### Step 3: Find the Request in HTTP History

1. In Burp, go to **Proxy → HTTP History**
2. Find the `POST /api/validate-header` request
3. Right-click → **Send to Repeater**

---

## Part 3: Testing Clean Headers (Baseline)

### In Repeater

The captured request should look like:

```
POST /api/validate-header HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Content-Length: 57

{"header_name": "X-Test-Header", "header_value": "test"}
```

**Send** this request.

### Secure App (Port 5000) — Expected Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "verdict": "ACCEPTED",
  "asvs_pass": true,
  "explanation": "The header name and value contain no CR or LF characters..."
}
```

### Vulnerable App (Port 5001) — Expected Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "verdict": "ACCEPTED",
  "asvs_pass": false,
  "explanation": "This header happened to be clean, but the application performed NO CRLF validation..."
}
```

Note the difference: even a clean header results in `"asvs_pass": false` in the vulnerable app because no validation logic exists.

---

## Part 4: Testing CRLF Injection via JSON Body

### Why Use JSON Body?

> **Important**: When using HTTP/2 (which this lab does), Burp's default HTTP/2 mode will prevent you from injecting literal `\r\n` characters into HTTP header lines — the h2 framing layer rejects malformed HEADERS frames. 
>
> This is by design and accurately represents RFC 9113 §8.2.1 behaviour.
>
> **However**, ASVS 4.2.4 requires validation at the **application layer**. The JSON body approach sends `\r\n` as characters within a JSON string value, which represents real-world scenarios where user-supplied data (from forms, APIs, databases) reaches application code containing these sequences.

### Test 1: LF Injection (\n)

In Repeater, modify the JSON body:

```json
{
  "header_name": "X-Attack-Header",
  "header_value": "legitimate-value\nSet-Cookie: session=hijacked"
}
```

> **Burp Tip**: Type `\n` literally in the JSON string — it will be interpreted as a newline character inside the JSON value.

**Secure App Response (port 5000)**:
```json
{
  "verdict": "REJECTED",
  "asvs_pass": true,
  "violations": ["Header 'X-Attack-Header' value '...' contains CR/LF sequence"]
}
```
HTTP Status: **400 Bad Request**

**Vulnerable App Response (port 5001)**:
```json
{
  "verdict": "ACCEPTED",
  "asvs_pass": false,
  "attack_type_demonstrated": "CRLF Injection / Header Injection"
}
```
HTTP Status: **200 OK** ← Accepted without rejection

### Test 2: CR Injection (\r)

```json
{
  "header_name": "X-Attack-Header",
  "header_value": "legitimate-value\rSet-Cookie: session=hijacked"
}
```

Same pattern — secure app rejects (400), vulnerable app accepts (200).

### Test 3: CRLF Injection (\r\n)

```json
{
  "header_name": "X-Attack-Header",
  "header_value": "legitimate-value\r\nSet-Cookie: session=hijacked"
}
```

This is the classic response splitting payload.

**Secure App**: 400 REJECTED  
**Vulnerable App**: 200 ACCEPTED + shows simulated HTTP/1.1 injection

### Test 4: Double CRLF — Response Splitting

```json
{
  "header_name": "X-Attack-Header",
  "header_value": "value\r\n\r\nHTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html>Injected</html>"
}
```

**Vulnerable App**: 200 ACCEPTED — shows the full response splitting simulation

### Test 5: Log Injection

```json
{
  "header_name": "X-User-Agent",
  "header_value": "Mozilla/5.0\n[INFO] ADMIN LOGIN SUCCESSFUL user=administrator"
}
```

**Vulnerable App**: 200 ACCEPTED  
After sending, run: `docker logs asvs-4.2.4-vulnerable` to see the injected log line.

---

## Part 5: Testing the Echo Endpoint

The `/api/echo-header` endpoint takes query parameters.

### Example Request in Repeater

```
GET /api/echo-header?name=X-Echo&value=test-value HTTP/1.1
Host: localhost:5001
```

### Inject via Query Parameter

```
GET /api/echo-header?name=X-Echo&value=test%0d%0aSet-Cookie:%20evil=1 HTTP/1.1
```

`%0d%0a` is URL-encoded `\r\n`.

The vulnerable app decodes this in the Python code and processes the CR/LF:

```python
decoded_value = header_value.replace("%0d", "\r").replace("%0a", "\n")
```

Look at the response — you'll see:
- `"attack_present": true`
- The response body explains what would happen in HTTP/1.1
- In the response headers, you may see `X-Injection-Blocked-By-Framework` if Werkzeug catches it

---

## Part 6: Attempting Raw Header CRLF Injection (HTTP/2 Limitation)

### Why This Doesn't Work

If you try to inject CRLF directly into an HTTP header in Burp's HTTP/2 mode:

1. In Repeater, right-click on a header value
2. Try to insert a literal newline character
3. Burp will either:
   a. Prevent you from entering it, OR
   b. The h2 library will reject the frame

This is the **expected behaviour** of RFC 9113 §8.2.1 compliance. The transport layer is doing its job.

### Educational Point

Write this observation in your lab notes:

> "Burp's HTTP/2 mode correctly prevents CRLF injection at the transport layer. This demonstrates that HTTP/2's binary framing does provide some protection. However, ASVS 4.2.4 requires *application-level* validation because:
> 1. Not all deployments use HTTP/2 end-to-end (HTTP/1.1 backends are common)
> 2. JSON/form bodies can carry `\r\n` that reaches application code
> 3. Logs and databases don't benefit from HTTP/2 framing protection"

### Using Raw TCP/h2c for True Wire-Level Testing

For advanced testing, tools like `h2c` or Python's `h2` library allow constructing raw HTTP/2 frames. However, this is beyond the scope of this educational lab.

---

## Part 7: Comparing Secure vs Vulnerable

Create a side-by-side comparison table in your lab notes:

| Test | Secure (5000) | Vulnerable (5001) | ASVS 4.2.4 |
|------|--------------|-------------------|-----------|
| `header_value: "clean"` | 200 ACCEPTED | 200 ACCEPTED (no validation) | Secure: ✅ Vuln: ❌ |
| `header_value: "v\r"` | 400 REJECTED | 200 ACCEPTED | Secure: ✅ Vuln: ❌ |
| `header_value: "v\n"` | 400 REJECTED | 200 ACCEPTED | Secure: ✅ Vuln: ❌ |
| `header_value: "v\r\n"` | 400 REJECTED | 200 ACCEPTED | Secure: ✅ Vuln: ❌ |
| `header_value: "v\r\n\r\n"` | 400 REJECTED | 200 ACCEPTED | Secure: ✅ Vuln: ❌ |

---

## Part 8: Checking Docker Logs for Log Injection

After sending log injection payloads to the vulnerable app:

```bash
docker logs asvs-4.2.4-vulnerable
```

Look for injected log lines that appear as separate entries. The vulnerable app logs header values without sanitization, so any `\n` in the value creates a new log line.

Compare with the secure app:
```bash
docker logs asvs-4.2.4-secure
```

The secure app's log shows only: "BLOCKED request — CRLF injection detected". The malicious content is never logged as a data value.

---

## Summary

| What Was Tested | Result |
|----------------|--------|
| Clean header via JSON body | Both apps accept |
| `\n` in JSON body value | Secure: reject / Vulnerable: accept |
| `\r` in JSON body value | Secure: reject / Vulnerable: accept |
| `\r\n` in JSON body value | Secure: reject / Vulnerable: accept |
| URL-encoded `%0d%0a` in query param | Both decode it; Secure: reject / Vulnerable: accept |
| Raw CRLF in HTTP/2 header | Blocked by h2 framing layer in both (expected) |
| Log injection | Secure: sanitized / Vulnerable: injected |
