# ASVS 4.2.3 - Expected Test Results

## Overview

This document specifies the exact expected outputs for all ASVS 4.2.3 tests. Use this as a verification checklist.

## HTTP Status Codes

### Secure Implementation (Port 8000)

| Test Case | Expected HTTP Status | Expected Response Field |
|-----------|---------------------|------------------------|
| Valid request | 200 OK | "status": "PASS" |
| Forbidden header present | 400 Bad Request | "status": "FAIL" |
| Multiple forbidden headers | 400 Bad Request | "status": "FAIL" |
| Valid headers only | 200 OK | "status": "PASS" |
| Health check | 200 OK | "status": "ok" |

### Vulnerable Implementation (Port 8001)

| Test Case | Expected HTTP Status | Expected Response Field |
|-----------|---------------------|------------------------|
| Valid request | 200 OK | "status": "ACCEPTED" |
| Forbidden header present | 200 OK | "status": "ACCEPTED" |
| Multiple forbidden headers | 200 OK | "status": "ACCEPTED" |
| Valid headers only | 200 OK | "status": "ACCEPTED" |
| Health check | 200 OK | "status": "ok" |

## Detailed Expected Responses

### Test 1: Health Check

**Request:**
```http
GET /health HTTP/2
Host: localhost:8000
```

**Expected Response (Both Secure and Vulnerable):**
```
HTTP/2 200 OK
Content-Type: application/json
Content-Length: 17

{
  "status": "ok"
}
```

### Test 2: Valid Request (No Forbidden Headers)

**Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Content-Type: application/json

{"data": "test"}
```

**Expected Response (Secure - Port 8000):**
```
HTTP/2 200 OK
Content-Type: application/json

{
  "status": "PASS",
  "message": "Request accepted - compliant with ASVS 4.2.3",
  "asvs_control": "4.2.3",
  "protocol": "HTTP/2",
  "request_data": {
    "data": "test"
  },
  "forbidden_headers_found": [],
  "explanation": "No forbidden connection-specific headers were present in this HTTP/2 request. HTTP/2 (RFC 7540) removed connection-specific headers because: 1) HTTP/2 uses multiplexing - multiple streams share one connection 2) Connection-scoped concepts (Keep-Alive, Upgrade) are meaningless in HTTP/2 3) These headers could be used for header injection and response splitting attacks"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK
Content-Type: application/json

{
  "status": "ACCEPTED",
  "message": "Request accepted without validation - VULNERABLE",
  "asvs_control": "4.2.3",
  "compliance": "FAIL",
  "protocol": "HTTP/2",
  "request_data": {
    "data": "test"
  },
  "all_received_headers": {
    "Host": "localhost:8001",
    "Content-Type": "application/json",
    "...": "..."
  },
  "forwarded_headers": {
    "...": "..."
  },
  "vulnerability_explanation": "This application accepts connection-specific headers without validation..."
}
```

### Test 3: Transfer-Encoding Header

**Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Transfer-Encoding: chunked
Content-Type: application/json

{"data": "test"}
```

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request
Content-Type: application/json

{
  "status": "FAIL",
  "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
  "forbidden_headers_found": ["Transfer-Encoding"],
  "asvs_control": "4.2.3",
  "protocol": "HTTP/2 or HTTP/3",
  "reason": "RFC 7540 forbids connection-specific headers in HTTP/2 to prevent response splitting and header injection attacks"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK
Content-Type: application/json

{
  "status": "ACCEPTED",
  "message": "Request accepted without validation - VULNERABLE",
  "asvs_control": "4.2.3",
  "compliance": "FAIL - Headers that should be forbidden are accepted",
  "all_received_headers": {
    "Transfer-Encoding": "chunked",
    "...": "..."
  },
  "dangerous_headers_found": 1,
  "dangerous_headers_list": {
    "Transfer-Encoding": "chunked"
  },
  "vulnerability": "This implementation identifies dangerous headers but does NOT reject them..."
}
```

### Test 4: Connection Header

**Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Connection: close
Content-Type: application/json

{}
```

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request

{
  "status": "FAIL",
  "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
  "forbidden_headers_found": ["Connection"],
  "asvs_control": "4.2.3"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "status": "ACCEPTED",
  "dangerous_headers_found": 1,
  "dangerous_headers_list": {
    "Connection": "close"
  }
}
```

### Test 5: Keep-Alive Header

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request

{
  "status": "FAIL",
  "forbidden_headers_found": ["Keep-Alive"],
  "asvs_control": "4.2.3"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "status": "ACCEPTED",
  "dangerous_headers_found": 1,
  "dangerous_headers_list": {
    "Keep-Alive": "timeout=5, max=100"
  }
}
```

### Test 6: Upgrade Header

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request

{
  "status": "FAIL",
  "forbidden_headers_found": ["Upgrade"],
  "asvs_control": "4.2.3"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "status": "ACCEPTED",
  "dangerous_headers_found": 1,
  "dangerous_headers_list": {
    "Upgrade": "h2c"
  }
}
```

### Test 7: Proxy-Connection Header

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request

{
  "status": "FAIL",
  "forbidden_headers_found": ["Proxy-Connection"],
  "asvs_control": "4.2.3"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "status": "ACCEPTED",
  "dangerous_headers_found": 1,
  "dangerous_headers_list": {
    "Proxy-Connection": "keep-alive"
  }
}
```

### Test 8: Trailer Header

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request

{
  "status": "FAIL",
  "forbidden_headers_found": ["Trailer"],
  "asvs_control": "4.2.3"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "status": "ACCEPTED",
  "dangerous_headers_found": 1,
  "dangerous_headers_list": {
    "Trailer": "X-Custom-Trailer"
  }
}
```

### Test 9: Multiple Forbidden Headers

**Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Transfer-Encoding: chunked
Connection: close
Keep-Alive: timeout=5
```

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request

{
  "status": "FAIL",
  "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
  "forbidden_headers_found": [
    "Transfer-Encoding",
    "Connection",
    "Keep-Alive"
  ],
  "asvs_control": "4.2.3"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "status": "ACCEPTED",
  "message": "Request accepted without validation - VULNERABLE",
  "dangerous_headers_found": 3,
  "dangerous_headers_list": {
    "Transfer-Encoding": "chunked",
    "Connection": "close",
    "Keep-Alive": "timeout=5"
  }
}
```

### Test 10: All Six Forbidden Headers

**Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Transfer-Encoding: chunked
Connection: close
Keep-Alive: timeout=5
Upgrade: h2c
Proxy-Connection: keep-alive
Trailer: X-Signature
```

**Expected Response (Secure - Port 8000):**
```
HTTP/2 400 Bad Request

{
  "status": "FAIL",
  "forbidden_headers_found": [
    "Transfer-Encoding",
    "Connection",
    "Keep-Alive",
    "Upgrade",
    "Proxy-Connection",
    "Trailer"
  ],
  "asvs_control": "4.2.3"
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "status": "ACCEPTED",
  "dangerous_headers_found": 6,
  "dangerous_headers_list": {
    "Transfer-Encoding": "chunked",
    "Connection": "close",
    "Keep-Alive": "timeout=5",
    "Upgrade": "h2c",
    "Proxy-Connection": "keep-alive",
    "Trailer": "X-Signature"
  }
}
```

### Test 11: /api/validate Endpoint

**Request:**
```http
POST /api/validate HTTP/2
Host: localhost:8000
Transfer-Encoding: chunked
```

**Expected Response (Secure - Port 8000):**
```
HTTP/2 200 OK

{
  "protocol": "HTTP/1.1",
  "all_headers": {
    "Host": "localhost:8000",
    "Transfer-Encoding": "chunked",
    ...
  },
  "forbidden_headers_count": 1,
  "forbidden_headers": {
    "Transfer-Encoding": "chunked"
  },
  "is_compliant": false,
  "asvs_control": "4.2.3",
  "rfc": "RFC 7540 (HTTP/2)",
  "explanation": {
    "transfer_encoding": "HTTP/2 uses chunk encoding internally..."
  }
}
```

**Expected Response (Vulnerable - Port 8001):**
```
HTTP/2 200 OK

{
  "protocol": "HTTP/1.1",
  "all_headers": {
    "Host": "localhost:8001",
    "Transfer-Encoding": "chunked",
    ...
  },
  "dangerous_headers_found": 1,
  "dangerous_headers_list": {
    "Transfer-Encoding": "chunked"
  },
  "asvs_control": "4.2.3",
  "compliance": "FAIL - Headers that should be forbidden are accepted"
}
```

### Test 12: /api/info Endpoint

**Request:**
```http
GET /api/info HTTP/2
Host: localhost:8000
```

**Expected Response (Both Implementations - Similar):**
```
HTTP/2 200 OK

{
  "asvs_control": "4.2.3",
  "requirement": "Verify that the application does not send nor accept HTTP/2 or HTTP/3 messages...",
  "level": 3,
  "forbidden_headers": [
    "transfer-encoding",
    "connection",
    "keep-alive",
    "upgrade",
    "proxy-connection",
    "trailer"
  ],
  "why_forbidden": {
    "background": "HTTP/2 (RFC 7540) fundamentally changed how HTTP works...",
    "transfer_encoding": "In HTTP/2, all messages are transmitted in frames...",
    "connection": "Explicitly tells the recipient to close the connection...",
    ...
  },
  "tests_included": [
    "curl command with custom headers",
    "Burp Suite intruder to test multiple headers",
    ...
  ]
}
```

## Response Format Verification

### Secure Implementation Response Patterns

**Always includes:**
- `"status": "PASS"` (for valid requests) or `"FAIL"` (for violations)
- `"asvs_control": "4.2.3"`
- `"forbidden_headers_found": [...]` (array, may be empty)

**Rejection always includes:**
- HTTP 400 status code
- Explanation of why headers are forbidden
- Reference to RFC 7540

### Vulnerable Implementation Response Patterns

**Always includes:**
- `"status": "ACCEPTED"` (even when violating)
- `"asvs_control": "4.2.3"`
- `"compliance": "FAIL"`
- `"all_received_headers": {...}` (all headers are listed)

**Never includes:**
- HTTP 400 status code (always 200)
- Rejection of forbidden headers
- Early validation

## Header Case Sensitivity

### Important: Headers are Case-Insensitive

The following should all be detected as "Transfer-Encoding":
- Transfer-Encoding
- transfer-encoding
- TRANSFER-ENCODING
- transfer-ENCODING

**Secure Implementation Response:**
```
HTTP/2 400 Bad Request

{
  "forbidden_headers_found": ["Transfer-Encoding"]  # May normalize to lowercase
}
```

## Response Content Type

**All responses should include:**
```
Content-Type: application/json
```

## Response Content-Length

Responses should include a valid Content-Length header corresponding to the body size.

## Timing

### Response Time Expectations

- **Secure:** Slightly slower due to validation (~10-50ms overhead)
- **Vulnerable:** Faster (no validation)

### Maximum acceptable response time: 1 second

## Error Response Examples

### 400 Bad Request (Secure Only)

**Format:**
```json
{
  "status": "FAIL",
  "message": "Description of what went wrong",
  "forbidden_headers_found": [...],
  "asvs_control": "4.2.3",
  "reason": "Explanation based on RFC 7540"
}
```

### 200 OK with ACCEPTED (Vulnerable Only)

**Format:**
```json
{
  "status": "ACCEPTED",
  "message": "Request accepted without validation - VULNERABLE",
  "all_received_headers": {...}
}
```

## Verification Checklist

When testing, verify:

- [ ] Secure version returns 400 for each forbidden header
- [ ] Vulnerable version returns 200 for each forbidden header
- [ ] Response includes all forbidden headers found
- [ ] Response includes asvs_control: "4.2.3"
- [ ] Response is valid JSON
- [ ] Content-Type is application/json
- [ ] All 6 forbidden headers are detected
- [ ] Multiple headers cause single rejection
- [ ] Valid headers pass (200 OK on both)
- [ ] /api/validate provides detailed analysis
- [ ] /api/info provides complete control information
- [ ] Health check works on both
- [ ] Headers are case-insensitive
- [ ] Response times are acceptable

## Summary

**Secure (Port 8000):**
- Forbidden headers → 400 Bad Request
- Valid headers → 200 OK with PASS status
- Compliance: ✓ PASS

**Vulnerable (Port 8001):**
- Forbidden headers → 200 OK with ACCEPTED status
- Valid headers → 200 OK with ACCEPTED status
- Compliance: ✗ FAIL

If actual responses differ from these expectations, investigate:
1. Is the application running?
2. Are you testing the correct ports?
3. Is the protocol actually HTTP/2?
4. Check application logs for errors
5. Verify request format matches examples
