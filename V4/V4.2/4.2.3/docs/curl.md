# ASVS 4.2.3 - curl Command Reference

## Overview

This guide provides curl commands for testing ASVS 4.2.3 HTTP/2 header validation. Note that basic curl has limited HTTP/2 support; Burp Suite is recommended for full HTTP/2 testing.

## Prerequisites

```bash
# Check curl HTTP/2 support
curl --version

# Should show: HTTP2
# If not present, reinstall curl with HTTP/2 support
```

## Basic Testing

### Test 1: Check Server is Running

```bash
# Secure version (port 8000)
curl -v http://localhost:8000/health

# Expected output:
# < HTTP/1.1 200 OK
# {"status":"ok"}

# Vulnerable version (port 8001)
curl -v http://localhost:8001/health

# Expected output:
# < HTTP/1.1 200 OK
# {"status":"ok"}
```

### Test 2: Valid Request (Should Pass on Both)

```bash
# Secure version - should return 200 OK
curl -v \
  -H "Accept: application/json" \
  -H "User-Agent: curl-test" \
  http://localhost:8000/api/test

# Response:
# < HTTP/2 200 OK
# {
#   "status": "PASS",
#   "message": "Request accepted - compliant with ASVS 4.2.3"
# }

# Vulnerable version - should also return 200 OK
curl -v \
  -H "Accept: application/json" \
  -H "User-Agent: curl-test" \
  http://localhost:8001/api/test

# Response:
# < HTTP/2 200 OK
# {
#   "status": "ACCEPTED",
#   "message": "Request accepted without validation - VULNERABLE"
# }
```

## Testing Forbidden Headers

### Test 3: Transfer-Encoding Header

```bash
# Secure - should reject with 400
curl -v \
  --http2 \
  -H "Transfer-Encoding: chunked" \
  http://localhost:8000/api/test

# Expected:
# < HTTP/2 400 Bad Request
# {
#   "status": "FAIL",
#   "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
#   "forbidden_headers_found": ["Transfer-Encoding"]
# }

# Vulnerable - should accept with 200
curl -v \
  --http2 \
  -H "Transfer-Encoding: chunked" \
  http://localhost:8001/api/test

# Expected:
# < HTTP/2 200 OK
# {
#   "status": "ACCEPTED",
#   "all_received_headers": {
#     "Transfer-Encoding": "chunked"
#   }
# }
```

### Test 4: Connection Header

```bash
# Secure - should reject
curl -v \
  --http2 \
  -H "Connection: close" \
  http://localhost:8000/api/test

# Expected: HTTP/2 400 Bad Request

# Vulnerable - should accept
curl -v \
  --http2 \
  -H "Connection: close" \
  http://localhost:8001/api/test

# Expected: HTTP/2 200 OK
```

### Test 5: Keep-Alive Header

```bash
# Secure - should reject
curl -v \
  --http2 \
  -H "Keep-Alive: timeout=5, max=100" \
  http://localhost:8000/api/test

# Expected: HTTP/2 400 Bad Request

# Vulnerable - should accept
curl -v \
  --http2 \
  -H "Keep-Alive: timeout=5, max=100" \
  http://localhost:8001/api/test

# Expected: HTTP/2 200 OK
```

### Test 6: Upgrade Header

```bash
# Secure - should reject
curl -v \
  --http2 \
  -H "Upgrade: h2c" \
  http://localhost:8000/api/test

# Expected: HTTP/2 400 Bad Request

# Vulnerable - should accept
curl -v \
  --http2 \
  -H "Upgrade: h2c" \
  http://localhost:8001/api/test

# Expected: HTTP/2 200 OK
```

### Test 7: Proxy-Connection Header

```bash
# Secure - should reject
curl -v \
  --http2 \
  -H "Proxy-Connection: keep-alive" \
  http://localhost:8000/api/test

# Expected: HTTP/2 400 Bad Request

# Vulnerable - should accept
curl -v \
  --http2 \
  -H "Proxy-Connection: keep-alive" \
  http://localhost:8001/api/test

# Expected: HTTP/2 200 OK
```

### Test 8: Trailer Header

```bash
# Secure - should reject
curl -v \
  --http2 \
  -H "Trailer: X-Custom-Trailer" \
  http://localhost:8000/api/test

# Expected: HTTP/2 400 Bad Request

# Vulnerable - should accept
curl -v \
  --http2 \
  -H "Trailer: X-Custom-Trailer" \
  http://localhost:8001/api/test

# Expected: HTTP/2 200 OK
```

## Testing Multiple Headers

### Test 9: Multiple Forbidden Headers

```bash
# Secure - should reject and list all forbidden headers
curl -v \
  --http2 \
  -H "Transfer-Encoding: chunked" \
  -H "Connection: close" \
  -H "Keep-Alive: timeout=5" \
  http://localhost:8000/api/test

# Expected:
# < HTTP/2 400 Bad Request
# {
#   "status": "FAIL",
#   "forbidden_headers_found": [
#     "Transfer-Encoding",
#     "Connection",
#     "Keep-Alive"
#   ]
# }

# Vulnerable - should accept all
curl -v \
  --http2 \
  -H "Transfer-Encoding: chunked" \
  -H "Connection: close" \
  -H "Keep-Alive: timeout=5" \
  http://localhost:8001/api/test

# Expected: HTTP/2 200 OK
```

### Test 10: All Six Forbidden Headers

```bash
# Secure - should reject all
curl -v \
  --http2 \
  -H "Transfer-Encoding: chunked" \
  -H "Connection: close" \
  -H "Keep-Alive: timeout=5" \
  -H "Upgrade: h2c" \
  -H "Proxy-Connection: keep-alive" \
  -H "Trailer: X-Signature" \
  http://localhost:8000/api/test

# Expected: HTTP/2 400 Bad Request with all 6 headers in forbidden_headers_found

# Vulnerable - should accept all
curl -v \
  --http2 \
  -H "Transfer-Encoding: chunked" \
  -H "Connection: close" \
  -H "Keep-Alive: timeout=5" \
  -H "Upgrade: h2c" \
  -H "Proxy-Connection: keep-alive" \
  -H "Trailer: X-Signature" \
  http://localhost:8001/api/test

# Expected: HTTP/2 200 OK
```

## Testing with Request Body

### Test 11: POST with JSON Body

```bash
# Secure - valid headers with body should pass
curl -v \
  --http2 \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  http://localhost:8000/api/test

# Expected: HTTP/2 200 OK with PASS status

# Secure - forbidden header with body should reject
curl -v \
  --http2 \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Transfer-Encoding: chunked" \
  -d '{"key": "value"}' \
  http://localhost:8000/api/test

# Expected: HTTP/2 400 Bad Request
```

### Test 12: Validate Endpoint

```bash
# Test the /api/validate endpoint
# Secure - forbidden header
curl -v \
  --http2 \
  -X POST \
  -H "Transfer-Encoding: chunked" \
  http://localhost:8000/api/validate

# Expected: Validation results with dangerous_headers_found

# Vulnerable - forbidden header
curl -v \
  --http2 \
  -X POST \
  -H "Transfer-Encoding: chunked" \
  http://localhost:8001/api/validate

# Expected: Shows dangerous headers but doesn't reject
```

## Testing Info Endpoint

### Test 13: Get Control Information

```bash
# Get detailed information about ASVS 4.2.3
curl -v http://localhost:8000/api/info

# Returns:
# {
#   "asvs_control": "4.2.3",
#   "requirement": "...",
#   "level": 3,
#   "forbidden_headers": ["transfer-encoding", "connection", ...],
#   "why_forbidden": {...}
# }
```

## Advanced Testing

### Test 14: Protocol Parameter

```bash
# Specify protocol version via query parameter
curl -v \
  --http2 \
  -H "Transfer-Encoding: chunked" \
  "http://localhost:8000/api/test?protocol=http2"

# Expected: Secure rejects this

curl -v \
  "http://localhost:8000/api/test?protocol=http1"

# Expected: May allow certain headers (simulating HTTP/1.1)
```

### Test 15: CRLF Injection Attempt (URL encoding)

```bash
# Note: curl automatically encodes, but try manual injection
curl -v \
  --http2 \
  -H "User-Agent: test%0d%0aX-Injected: malicious" \
  http://localhost:8001/api/test

# Vulnerable might reflect the injected header
```

## Batch Testing Script

### Script: Test All Forbidden Headers

```bash
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SECURE="http://localhost:8000"
VULNERABLE="http://localhost:8001"

# Array of forbidden headers
forbidden_headers=(
  "Transfer-Encoding: chunked"
  "Connection: close"
  "Keep-Alive: timeout=5"
  "Upgrade: h2c"
  "Proxy-Connection: keep-alive"
  "Trailer: X-Custom-Trailer"
)

echo "Testing ASVS 4.2.3 Header Validation"
echo "===================================="

for header in "${forbidden_headers[@]}"; do
  header_name=$(echo "$header" | cut -d':' -f1)
  echo -e "\nTesting: $header_name"
  
  # Test secure
  response_secure=$(curl -s -w "\n%{http_code}" -H "$header" "$SECURE/api/test")
  status_secure=$(echo "$response_secure" | tail -n1)
  
  # Test vulnerable
  response_vulnerable=$(curl -s -w "\n%{http_code}" -H "$header" "$VULNERABLE/api/test")
  status_vulnerable=$(echo "$response_vulnerable" | tail -n1)
  
  # Display results
  if [ "$status_secure" -eq 400 ]; then
    echo -e "  Secure: ${GREEN}400 (Correctly Rejected)${NC}"
  else
    echo -e "  Secure: ${RED}$status_secure (Should be 400)${NC}"
  fi
  
  if [ "$status_vulnerable" -eq 200 ]; then
    echo -e "  Vulnerable: ${RED}200 (Should be rejected)${NC}"
  else
    echo -e "  Vulnerable: ${GREEN}$status_vulnerable (Unexpectedly rejected)${NC}"
  fi
done

echo -e "\n===================================="
echo "Testing complete!"
```

### Save and run:

```bash
chmod +x test_asvs_4_2_3.sh
./test_asvs_4_2_3.sh
```

## Comparison Script

### Script: Compare Responses

```bash
#!/bin/bash

echo "Testing: Transfer-Encoding header"
echo "=================================="

echo -e "\n=== SECURE (Port 8000) ==="
curl -s -H "Transfer-Encoding: chunked" http://localhost:8000/api/test | jq .

echo -e "\n=== VULNERABLE (Port 8001) ==="
curl -s -H "Transfer-Encoding: chunked" http://localhost:8001/api/test | jq .

echo -e "\n=================================="
echo "Secure should show: status='FAIL'"
echo "Vulnerable should show: status='ACCEPTED'"
```

## Limitations of curl

### HTTP/2 Support

- Basic curl may use HTTP/1.1 even with `--http2` flag
- Some curl builds don't include HTTP/2 support
- Verify: `curl --version | grep -i h2`

### Workaround

If curl doesn't support HTTP/2, use:

1. **http2-docker:** Docker image with HTTP/2 testing tools
2. **Python requests:** With h2 library
3. **Burp Suite:** Better HTTP/2 support
4. **Nginx:** Local HTTP/2 proxy

### Python Alternative

```python
import http.client
import json

# Not all Python versions support HTTP/2 natively
# Use hyper or h2 library for better support

# Basic test with standard library (HTTP/1.1 fallback)
import urllib.request

headers = {"Transfer-Encoding": "chunked"}
req = urllib.request.Request(
    "http://localhost:8000/api/test",
    headers=headers
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(json.dumps(json.loads(response.read()), indent=2))
except urllib.error.HTTPError as e:
    print(f"Status: {e.code}")
    print(json.dumps(json.loads(e.read()), indent=2))
```

## Expected Output Summary

### Secure Implementation (Port 8000)

**With Forbidden Headers:**
```
Status Code: 400 Bad Request
Response: {
  "status": "FAIL",
  "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
  "forbidden_headers_found": ["Transfer-Encoding"] (or other header)
}
```

**With Valid Headers:**
```
Status Code: 200 OK
Response: {
  "status": "PASS",
  "message": "Request accepted - compliant with ASVS 4.2.3"
}
```

### Vulnerable Implementation (Port 8001)

**With Any Headers:**
```
Status Code: 200 OK
Response: {
  "status": "ACCEPTED",
  "message": "Request accepted without validation - VULNERABLE",
  "all_received_headers": {...}
}
```

## Testing Checklist

- [ ] Health check both endpoints
- [ ] Valid request test
- [ ] Each of 6 forbidden headers (individual)
- [ ] Multiple forbidden headers together
- [ ] All 6 forbidden headers together
- [ ] POST with JSON body
- [ ] /api/validate endpoint
- [ ] /api/info endpoint
- [ ] Compare response status codes
- [ ] Verify response content
- [ ] Run batch test script
- [ ] Document all results

## Summary

curl Testing for ASVS 4.2.3:

1. **Prerequisites:** Verify HTTP/2 support in curl
2. **Baseline:** Test valid requests first
3. **Individual:** Test each forbidden header
4. **Batch:** Test multiple headers
5. **Comparison:** Compare secure vs vulnerable
6. **Documentation:** Collect response examples
7. **Limitations:** Remember curl limitations with HTTP/2
8. **Alternatives:** Use Burp Suite for complete HTTP/2 testing

Note: While curl is useful for basic testing, Burp Suite or a Python HTTP/2 library provides more comprehensive HTTP/2 protocol testing capabilities.
