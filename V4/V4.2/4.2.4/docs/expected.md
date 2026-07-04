# ASVS 4.2.4 — Expected Outcomes

## Purpose

This document defines the exact expected behaviour for every test scenario in the lab. Use this as a reference for verifying your results and grading student work.

---

## Secure App (port 5000) — Expected to PASS ASVS 4.2.4

### Test 1: Clean Header

**Input**:
```json
{"header_name": "X-Custom-Header", "header_value": "legitimate-value"}
```

**Expected HTTP Status**: `200 OK`

**Expected Response Body** (partial):
```json
{
  "verdict": "ACCEPTED",
  "asvs_pass": true,
  "asvs_control": "4.2.4"
}
```

**ASVS 4.2.4**: ✅ PASS

---

### Test 2: LF Injection (`\n`)

**Input**:
```json
{"header_name": "X-Attack", "header_value": "value\nSet-Cookie: evil=1"}
```

**Expected HTTP Status**: `400 Bad Request`

**Expected Response Body**:
```json
{
  "verdict": "REJECTED",
  "asvs_pass": true,
  "asvs_control": "4.2.4",
  "reason": "Request headers contain forbidden CR (\\r) or LF (\\n) sequences.",
  "violations": ["Header 'X-Attack' value '...' contains CR/LF sequence"]
}
```

**ASVS 4.2.4**: ✅ PASS (rejection is the correct behaviour)

---

### Test 3: CR Injection (`\r`)

**Input**:
```json
{"header_name": "X-Attack", "header_value": "value\rSet-Cookie: evil=1"}
```

**Expected HTTP Status**: `400 Bad Request`

**ASVS 4.2.4**: ✅ PASS

---

### Test 4: CRLF Injection (`\r\n`)

**Input**:
```json
{"header_name": "X-Attack", "header_value": "value\r\nSet-Cookie: session=hijacked"}
```

**Expected HTTP Status**: `400 Bad Request`

**ASVS 4.2.4**: ✅ PASS

---

### Test 5: Double CRLF — Response Splitting Attempt

**Input**:
```json
{"header_name": "X-Attack", "header_value": "value\r\n\r\n<html>Injected</html>"}
```

**Expected HTTP Status**: `400 Bad Request`

**ASVS 4.2.4**: ✅ PASS

---

### Test 6: CRLF in Header Name

**Input**:
```json
{"header_name": "X-Attack\r\nSet-Cookie: evil=1", "header_value": "test"}
```

**Expected HTTP Status**: `400 Bad Request`

**ASVS 4.2.4**: ✅ PASS

---

### Test 7: Echo Endpoint — Clean Value

**Request**: `GET /api/echo-header?name=X-Safe&value=safe-value`

**Expected HTTP Status**: `200 OK`

**Expected**: Response includes `X-Safe: safe-value` header

**ASVS 4.2.4**: ✅ PASS

---

### Test 8: Echo Endpoint — CRLF Injection

**Request**: `GET /api/echo-header?name=X-Safe&value=test%0d%0aSet-Cookie:%20evil=1`

**Expected HTTP Status**: `400 Bad Request`

**ASVS 4.2.4**: ✅ PASS

---

## Vulnerable App (port 5001) — Expected to FAIL ASVS 4.2.4

### Test 1: Clean Header

**Input**:
```json
{"header_name": "X-Custom-Header", "header_value": "legitimate-value"}
```

**Expected HTTP Status**: `200 OK`

**Expected Response Body** (partial):
```json
{
  "verdict": "ACCEPTED",
  "asvs_pass": false,
  "missing_control": "No CRLF validation on header name or value"
}
```

**ASVS 4.2.4**: ❌ FAIL — Even though the header is clean, no validation logic exists

---

### Test 2: LF Injection (`\n`)

**Input**:
```json
{"header_name": "X-Attack", "header_value": "value\nSet-Cookie: evil=1"}
```

**Expected HTTP Status**: `200 OK` (ACCEPTED without rejection)

**Expected Response Body** (partial):
```json
{
  "verdict": "ACCEPTED",
  "asvs_pass": false,
  "attack_type_demonstrated": "CRLF Injection / Header Injection",
  "simulated_http1_injection": "HTTP/1.1 200 OK\r\n...X-Attack: value\r\nSet-Cookie: evil=1..."
}
```

**ASVS 4.2.4**: ❌ FAIL — Accepted injection payload

---

### Test 3: CR Injection (`\r`)

**Input**:
```json
{"header_name": "X-Attack", "header_value": "value\rSet-Cookie: evil=1"}
```

**Expected HTTP Status**: `200 OK` (ACCEPTED)

**ASVS 4.2.4**: ❌ FAIL

---

### Test 4: CRLF Injection (`\r\n`)

**Input**:
```json
{"header_name": "X-Attack", "header_value": "value\r\nSet-Cookie: session=hijacked"}
```

**Expected HTTP Status**: `200 OK` (ACCEPTED)

**Expected**: Response includes `simulated_http1_injection` showing the injection

**ASVS 4.2.4**: ❌ FAIL

---

### Test 5: Log Injection

**Input**:
```json
{"header_name": "X-User-Agent", "header_value": "Mozilla/5.0\n[INFO] ADMIN LOGIN from attacker"}
```

**Expected HTTP Status**: `200 OK` (ACCEPTED)

**Docker Log Effect**: Running `docker logs asvs-4.2.4-vulnerable` should show an injected log line

**ASVS 4.2.4**: ❌ FAIL

---

## Summary Comparison Table

| Test | Secure (5000) | Vulnerable (5001) | ASVS 4.2.4 |
|------|:---:|:---:|:---:|
| Clean header | 200 ✅ | 200 (no validation) ❌ | Secure: PASS / Vuln: FAIL |
| `\n` in value | 400 ✅ | 200 ❌ | Secure: PASS / Vuln: FAIL |
| `\r` in value | 400 ✅ | 200 ❌ | Secure: PASS / Vuln: FAIL |
| `\r\n` in value | 400 ✅ | 200 ❌ | Secure: PASS / Vuln: FAIL |
| `\r\n` in name | 400 ✅ | 200 ❌ | Secure: PASS / Vuln: FAIL |
| Double `\r\n` | 400 ✅ | 200 ❌ | Secure: PASS / Vuln: FAIL |
| Log injection | Blocked ✅ | Injected ❌ | Secure: PASS / Vuln: FAIL |
| Echo clean | 200 ✅ | 200 ❌ | Secure: PASS / Vuln: FAIL |
| Echo `%0d%0a` | 400 ✅ | 200 ❌ | Secure: PASS / Vuln: FAIL |

---

## Framework-Level Observations

### When Testing via HTTP Headers Directly

Both apps will block raw CRLF injection via actual HTTP headers because:
1. Hypercorn (HTTP/2 server) enforces RFC 9113 §8.2.1 at the framing layer
2. curl refuses to send headers with `\r\n`

**This is expected and correct**. The educational value is demonstrating that application-layer validation is still required per ASVS 4.2.4.

### The `X-Injection-Blocked-By-Framework` Header

In some tests, the vulnerable app's response may include:
```
X-Injection-Blocked-By-Framework: Framework rejected invalid header: ValueError
X-Educational-Note: Even though the framework blocked this at transport level...
```

This is intentional. It demonstrates that:
- The framework CAN block it at the transport level
- But the APPLICATION CODE contains no validation logic
- ASVS 4.2.4 requires the application to validate, not rely on the framework
