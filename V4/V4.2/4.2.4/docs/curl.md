# ASVS 4.2.4 — curl Testing Guide

## Overview

This guide provides curl commands to test ASVS 4.2.4 compliance. It also explains the important limitations of using curl for CRLF injection testing and when alternative tools are more appropriate.

---

## Prerequisites

- curl 7.80+ (with HTTP/2 support: `curl --version | grep HTTP2`)
- Docker containers running:
  - Secure: http://localhost:5000
  - Vulnerable: http://localhost:5001

---

## Part 1: Basic Health Checks

### Check Both Apps are Running

```bash
# Secure app
curl -s http://localhost:5000/api/info | python3 -m json.tool

# Vulnerable app
curl -s http://localhost:5001/api/info | python3 -m json.tool
```

**Expected for secure**: `"crlf_validation": true`  
**Expected for vulnerable**: `"crlf_validation": false`

---

## Part 2: Testing Clean Headers via JSON API

### Send a Clean Header (Should Pass Both Apps)

```bash
# Secure app
curl -s -X POST http://localhost:5000/api/validate-header \
  -H "Content-Type: application/json" \
  -d '{"header_name": "X-Custom-Header", "header_value": "legitimate-value"}' \
  | python3 -m json.tool
```

**Expected**:
```json
{
    "verdict": "ACCEPTED",
    "asvs_pass": true,
    "header_name": "X-Custom-Header",
    "header_value_repr": "'legitimate-value'"
}
```

```bash
# Vulnerable app
curl -s -X POST http://localhost:5001/api/validate-header \
  -H "Content-Type: application/json" \
  -d '{"header_name": "X-Custom-Header", "header_value": "legitimate-value"}' \
  | python3 -m json.tool
```

**Expected**:
```json
{
    "verdict": "ACCEPTED",
    "asvs_pass": false,
    "missing_control": "No CRLF validation on header name or value"
}
```

---

## Part 3: CRLF Injection via JSON Body

> **Why JSON Body?**
> Direct CRLF injection into HTTP request headers via curl is prevented by:
> 1. curl itself (strips/rejects `\r\n` from `-H` header arguments)
> 2. HTTP/2 binary framing (Hypercorn rejects malformed HEADERS frames)
>
> The JSON body approach represents real-world scenarios where user-supplied data
> from forms, APIs, or databases reaches application code containing `\r\n`.

### LF Injection (`\n`) — Linux/macOS

```bash
curl -s -X POST http://localhost:5000/api/validate-header \
  -H "Content-Type: application/json" \
  -d $'{"header_name":"X-Attack","header_value":"value\\nSet-Cookie: evil=1"}' \
  | python3 -m json.tool
```

**Secure (5000) — Expected: HTTP 400 REJECTED**:
```json
{
    "verdict": "REJECTED",
    "asvs_pass": true,
    "violations": ["Header 'X-Attack' value 'value\\nSet-Cookie: evil=1' contains CR/LF sequence"]
}
```

**Vulnerable (5001) — Expected: HTTP 200 ACCEPTED**:
```json
{
    "verdict": "ACCEPTED",
    "asvs_pass": false,
    "attack_type_demonstrated": "CRLF Injection / Header Injection"
}
```

### CR Injection (`\r`) — Linux/macOS

```bash
curl -s -X POST http://localhost:5001/api/validate-header \
  -H "Content-Type: application/json" \
  -d $'{"header_name":"X-Attack","header_value":"value\\rSet-Cookie: evil=1"}' \
  | python3 -m json.tool
```

**Vulnerable (5001) — Expected: HTTP 200 ACCEPTED**

### CRLF Injection (`\r\n`) — Linux/macOS

```bash
curl -s -X POST http://localhost:5001/api/validate-header \
  -H "Content-Type: application/json" \
  -d $'{"header_name":"X-Attack","header_value":"value\\r\\nSet-Cookie: session=hijacked"}' \
  | python3 -m json.tool
```

**Vulnerable (5001) — Expected: HTTP 200 ACCEPTED + simulated injection**

### Windows (PowerShell)

On Windows, use escaped Unicode escapes in the JSON string:

```powershell
# LF injection
$body = '{"header_name":"X-Attack","header_value":"value\u000aSet-Cookie: evil=1"}'
curl.exe -s -X POST http://localhost:5001/api/validate-header `
  -H "Content-Type: application/json" `
  -d $body

# CRLF injection
$body = '{"header_name":"X-Attack","header_value":"value\u000d\u000aSet-Cookie: session=hijacked"}'
curl.exe -s -X POST http://localhost:5001/api/validate-header `
  -H "Content-Type: application/json" `
  -d $body
```

---

## Part 4: Testing the Echo Endpoint

### Clean Echo — Secure App

```bash
curl -s "http://localhost:5000/api/echo-header?name=X-Test&value=safe-value" \
  -v 2>&1 | head -40
```

**Expected**: HTTP 200, `X-Test: safe-value` visible in response headers.

### URL-Encoded CRLF — Vulnerable App

```bash
curl -s "http://localhost:5001/api/echo-header?name=X-Echo&value=test%0d%0aSet-Cookie:%20evil=1" \
  -v 2>&1 | head -40
```

The vulnerable app URL-decodes `%0d%0a` to `\r\n` in the application code.

**Expected from vulnerable app**: HTTP 200, response body shows `"attack_present": true`

### URL-Encoded CRLF — Secure App

```bash
curl -s "http://localhost:5000/api/echo-header?name=X-Echo&value=test%0d%0aSet-Cookie:%20evil=1" \
  -v 2>&1 | head -40
```

**Expected from secure app**: HTTP 400 REJECTED

---

## Part 5: Attempting Raw CRLF in curl Headers (Limitation Demo)

### Why This Doesn't Work

```bash
# This will FAIL — curl rejects CRLF in -H arguments
curl -s -X POST http://localhost:5000/api/validate-header \
  -H "X-Attack: value\r\nSet-Cookie: evil=1" \
  -d '{"header_name":"test","header_value":"clean"}'
```

**What happens**: curl refuses to send a header containing `\r\n` because it would violate HTTP specification. You'll see an error like:

```
curl: option -H: headers must not contain embedded carriage returns or linefeeds
```

This is **correct behaviour** from curl. The same prevention exists in:
- Python's `requests` library
- Go's `net/http`
- Node.js `http` module

### Educational Note

```
┌─────────────────────────────────────────────────────────────────┐
│  Why curl cannot inject CRLF into HTTP headers:                 │
│                                                                  │
│  1. curl validates -H arguments and rejects \r\n                │
│  2. HTTP/2 binary framing prevents it at the protocol level     │
│  3. Even HTTP/1.1 clients typically reject malformed headers    │
│                                                                  │
│  This does NOT mean applications are safe from CRLF injection.  │
│  The attack surface is:                                          │
│  • User input from forms/JSON that reaches header-setting code  │
│  • Database values retrieved and reflected in headers           │
│  • Third-party data used in response headers                    │
│  • URL-decoded query parameters set in Location/Set-Cookie      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Log Injection Test

### Send Log Injection Payload

```bash
curl -s -X POST http://localhost:5001/api/validate-header \
  -H "Content-Type: application/json" \
  -d $'{"header_name":"X-User-Agent","header_value":"Mozilla/5.0\\n[INFO] ADMIN LOGIN SUCCESS user=administrator"}' \
  | python3 -m json.tool
```

### Check Docker Logs

```bash
docker logs asvs-4.2.4-vulnerable 2>&1 | tail -20
```

You should see two separate log entries: the real one and the injected fake entry.

### Compare with Secure App

```bash
curl -s -X POST http://localhost:5000/api/validate-header \
  -H "Content-Type: application/json" \
  -d $'{"header_name":"X-User-Agent","header_value":"Mozilla/5.0\\n[INFO] ADMIN LOGIN SUCCESS user=administrator"}' \
  | python3 -m json.tool

docker logs asvs-4.2.4-secure 2>&1 | tail -10
```

The secure app log shows: `BLOCKED request from ... CRLF injection detected` — the malicious value is never logged as data.

---

## Part 7: Response Header Inspection

After a successful validation, check the custom header in the response:

```bash
curl -v -X POST http://localhost:5000/api/validate-header \
  -H "Content-Type: application/json" \
  -d '{"header_name":"X-Safe-Header","header_value":"safe-value"}' \
  2>&1 | grep -E "^< "
```

You should see `< X-Safe-Header: safe-value` in the response headers, confirming the secure app safely reflected the validated header value.

---

## Part 8: When to Use Burp Repeater Instead

Use **Burp Repeater over curl** when you need to:

| Scenario | Tool |
|----------|------|
| Inject `\r\n` in JSON bodies | Either (curl with `$'...'` syntax or Burp) |
| Visual comparison of responses | Burp |
| Modify individual header fields | Burp |
| Try raw TCP-level HTTP/1.1 CRLF injection | Netcat / raw TCP tools |
| HTTP/2 frame inspection | Wireshark + h2 dissector |
| Automated payload testing | Burp Intruder |

---

## Summary Table

| Test | curl Command | Secure (5000) | Vulnerable (5001) |
|------|-------------|--------------|-------------------|
| Clean header | `-d '{"header_value":"ok"}'` | 200 ACCEPTED | 200 ACCEPTED |
| LF in JSON | `-d $'{"header_value":"v\\n..."}'` | 400 REJECTED | 200 ACCEPTED |
| CR in JSON | `-d $'{"header_value":"v\\r..."}'` | 400 REJECTED | 200 ACCEPTED |
| CRLF in JSON | `-d $'{"header_value":"v\\r\\n..."}'` | 400 REJECTED | 200 ACCEPTED |
| Raw CRLF in `-H` | `-H "X-H: v\r\n"` | curl refuses | curl refuses |
| URL `%0d%0a` | `?value=v%0d%0a...` | 400 REJECTED | 200 ACCEPTED |
